//Network Topology
//
//Wifi infrastracture
//802.11b

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/wifi-module.h"
#include "ns3/mobility-module.h"
#include "ns3/applications-module.h"
#include "ns3/internet-module.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/netanim-module.h"

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <limits>
#include <iomanip>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("WifiInfraScenario");

int main(int argc, char *argv[])
{

  uint32_t nWifi = 10;
  bool tracing = false;
  StringValue DataRate;
  uint32_t packetSize = 1472;//maxPacketSize = 1472
  uint32_t maxPacket = 10000;
  double distance = 2.0;
  double StartTime = 0.0;
  double StopTime = 10.0;
  //double simulationTime = 10.0;
  DataRate = StringValue("DsssRate11Mbps");

  CommandLine cmd;
  cmd.AddValue("nWifi", "Number of Wifi STA device", nWifi);
  cmd.AddValue("tracing", "Enable pcap tracing", tracing);

  cmd.Parse(argc,argv);

  if(nWifi > 250)
  {
    std::cout << "Too  many wifi stations, no more than 80" << std::endl;
    return 1;
  }

  /***********Topology part***********/  

  //Creat Ap and stations
  NodeContainer wifiAp;
  wifiAp.Create(1);
  std::cout<<"Access Point created."<<"\n";

  NodeContainer wifiSta;
  wifiSta.Create(nWifi);
  std::cout<<"Stations created."<<"\n";

  //Initial physical channel
  WifiHelper wifi= WifiHelper::Default();
  wifi.SetStandard (WIFI_PHY_STANDARD_80211b);     // set wifi standard
  wifi.SetRemoteStationManager("ns3::ConstantRateWifiManager",  //set wifi rate manager
  	                           "DataMode", DataRate,
  	                           "ControlMode", DataRate);

  YansWifiPhyHelper wifiPhy = YansWifiPhyHelper::Default(); //NistErrorRateModel

  wifiPhy.Set ("RxGain", DoubleValue(0));
  //wifiPhy.SetPcapDataLinkType(YansWifiPhyHelper::DLT_IEEE802_11_RADIO);

  YansWifiChannelHelper wifiChannel = YansWifiChannelHelper::Default ();
  wifiChannel.SetPropagationDelay("ns3::ConstantSpeedPropagationDelayModel");  //set PropogationDelayModel to ConstantSpeed
  wifiChannel.AddPropagationLoss ("ns3::FriisPropagationLossModel");
 /* 
  wifiChannel.AddPropagationLoss("ns3::LogDistancePropagationLossModel",
  	                             "Exponent", DoubleValue(3.0),
  	                             "ReferenceLoss", DoubleValue(40.0459));
 */
  wifiPhy.SetChannel (wifiChannel.Create());
  std::cout<<"Wifi 802.11b physical channel configured."<<"\n";

  //Mac layer
  NqosWifiMacHelper wifiMac = NqosWifiMacHelper::Default(); //set to a non-Qos upper mac
  Ssid ssid = Ssid("WifiInfraScenario");

  //setup wifiSta
  wifiMac.SetType("ns3::StaWifiMac",
                  "Ssid", SsidValue(ssid),
                  "ActiveProbing", BooleanValue(false));
  NetDeviceContainer staDevice = wifi.Install(wifiPhy, wifiMac, wifiSta);

  //setup wifiAp
  wifiMac.SetType("ns3::ApWifiMac",
                  "Ssid",SsidValue(ssid));
  NetDeviceContainer apDevice = wifi.Install(wifiPhy, wifiMac, wifiAp); //install the device on node

  std::cout<<"apDevice and staDevice configured."<<"\n";
  
  //configure mobility
  MobilityHelper mobility;

  
  mobility.SetPositionAllocator("ns3::GridPositionAllocator",
                                "MinX",DoubleValue(0.0),
                                "MinY",DoubleValue(0.0),
                                "DeltaX",DoubleValue(distance),
                                "DeltaY",DoubleValue(distance),
                                "GridWidth",UintegerValue(3),
                                "LayoutType", StringValue("RowFirst"));

  
  //set the AP mobility
  mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
  mobility.Install(wifiAp);

  mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel",
            // "Bounds", RectangleValue (Rectangle (-10, 10, -10, 10)));
              //    "Bounds", RectangleValue (Rectangle (-50, 50, -50, 50)));
             //   "Bounds", RectangleValue (Rectangle (-100, 100, -100, 100)));
               "Bounds", RectangleValue (Rectangle (-150, 150, -150, 150)));

  //Install mobility to stations
  mobility.Install(wifiSta);

  std::cout<<"Mobility configured."<<"\n";

  //setup InternetStack
  InternetStackHelper stack;
  stack.Install(wifiAp);
  stack.Install(wifiSta);

  //Arrange the address
  Ipv4AddressHelper address;
  address.SetBase("10.1.1.0","255.255.255.0");
  Ipv4InterfaceContainer staInterface;
  Ipv4InterfaceContainer apInterface;
  staInterface = address.Assign(staDevice);
  apInterface = address.Assign(apDevice);

  std::cout<<"internet and address configured."<<"\n";

  /***********Application part***********/

  //setup Application

  //Install server
  ApplicationContainer serverApp;
  UdpServerHelper myServer(4001);
  //serverApp = myServer.Install(wifiSta.Get(0));
  serverApp.Start(Seconds(StartTime));
  serverApp.Stop(Seconds(StopTime));

  UdpClientHelper myClients(apInterface.GetAddress(0),4001);
  myClients.SetAttribute ("MaxPackets", UintegerValue (maxPacket));
  myClients.SetAttribute ("Interval", TimeValue (Time ("0.002")));
  myClients.SetAttribute ("PacketSize", UintegerValue (packetSize));

  //Install client
  ApplicationContainer clientApps = myClients.Install(wifiSta.Get(0));
  clientApps.Start(Seconds(StartTime));
  clientApps.Stop(Seconds(StopTime+3)); 
  std::cout<<"traffic created."<<"\n";
  
  /***********Throughput and delay calculate***********/
  //FloeMonitorHelper flowMonitor;

  
 //Ipv4GlobalRoutingHelper::PopulateRoutingTables();
  AnimationInterface anim ("WifiScenario.xml"); 
  std::cout<<".xml created."<<"\n";

  //wifiPhy.EnablePcap("third",apDevice.Get(0));

  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll();

  Simulator::Stop (Seconds(StopTime+2));
  Simulator::Run ();

  monitor->CheckForLostPackets ();
  Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier> (flowmon.GetClassifier ());
  std::map<FlowId, FlowMonitor::FlowStats> stats = monitor->GetFlowStats ();
  for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator iter = stats.begin (); iter != stats.end (); ++iter)
  {
   Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow (iter->first);
   std::cout << "Flow " << iter->first << "(" <<"Src addr"<< t.sourceAddress << " -> "<< "Dst addr" << t.destinationAddress << ")\n";
   std::cout << " Tx Bytes: " << iter->second.txBytes << "\n";
   std::cout << " Rx Bytes: " << iter->second.rxBytes << "\n";
   std::cout << " Average Throughput: " << iter->second.rxBytes * 8.0 / (iter->second.timeLastRxPacket.GetSeconds() - iter->second.timeFirstTxPacket.GetSeconds())/1024/nWifi << " kbps\n";
   std::cout << " MeanDelay : " << iter->second.delaySum / iter->second.rxPackets << "\n";
   std::cout << " PacktelossRate : " << 100 * (iter->second.txBytes - iter->second.rxBytes)/iter->second.txBytes << "%\n";;
  }
  
  Simulator::Destroy();
  return 0;

}
