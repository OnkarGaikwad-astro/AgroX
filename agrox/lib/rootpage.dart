import 'package:agrox/homePage.dart';
import 'package:agrox/tools/colorTheme.dart';
import 'package:flutter/material.dart';

class Rootpage extends StatefulWidget {
  final String username;

  const Rootpage({super.key,required this.username});

  @override
  State<Rootpage> createState() => _RootpageState();
}

class _RootpageState extends State<Rootpage> {
  int curr_page_index = 0;

  final List<Widget> pages = [
    Homepage(username: "Onkar")
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      bottomNavigationBar: NavigationBar(
        height: 70,
        backgroundColor: const Color.fromARGB(255, 255, 255, 255),
        indicatorColor: kAccentVariant,
        animationDuration: Duration(milliseconds: 100),
        selectedIndex: curr_page_index,
        onDestinationSelected: (value) {
          setState(() {
            curr_page_index = value;
          });
        },
        destinations: [
          NavigationDestination(icon: Icon(Icons.home), label: "Home",),
          NavigationDestination(icon: Icon(Icons.sell_rounded), label: "sell",enabled: false,),
          NavigationDestination(icon: Icon(Icons.functions), label: "fuck",enabled: false,),
          NavigationDestination(icon: Icon(Icons.snapchat), label: "snap",enabled: false,),
        ],
      ),
      appBar: AppBar(backgroundColor: kSeafoam),
      body: IndexedStack(
        index: curr_page_index,
        children:pages,
      ),
    );
  }
}