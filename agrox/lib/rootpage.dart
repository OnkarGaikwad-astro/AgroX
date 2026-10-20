import 'package:agrox/homePage.dart';
import 'package:agrox/tools/colorTheme.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class Rootpage extends StatefulWidget {
  final String username;

  const Rootpage({super.key, required this.username});

  @override
  State<Rootpage> createState() => _RootpageState();
}

class _RootpageState extends State<Rootpage> {
  int curr_page_index = 0;

  final List<Widget> pages = [Homepage(username: "Onkar")];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      bottomNavigationBar: NavigationBar(
        height: 50,
        backgroundColor: kAccentVariant,
        indicatorColor: kMint,
        shadowColor: kBackground,
        surfaceTintColor: kMint,
        animationDuration: Duration(milliseconds: 100),
        selectedIndex: curr_page_index,
        indicatorShape: RoundedRectangleBorder(
          borderRadius: BorderRadiusGeometry.circular(15),
        ),
        labelBehavior: NavigationDestinationLabelBehavior.alwaysHide,
        onDestinationSelected: (value) {
          setState(() {
            curr_page_index = value;
          });
        },
        destinations: [
          NavigationDestination(icon: Icon(Icons.home), label: "Home"),
          NavigationDestination(
            icon: Icon(Icons.sell_rounded),
            label: "sell",
            enabled: false,
          ),
          NavigationDestination(
            icon: Icon(Icons.functions),
            label: "fuck",
            enabled: false,
          ),
          NavigationDestination(
            icon: Icon(Icons.snapchat),
            label: "snap",
            enabled: false,
          ),
        ],
      ),
      appBar: AppBar(
        backgroundColor: kPrimaryVariant,
        toolbarHeight: 50,
        leading: Padding(
          padding: const EdgeInsets.only(left: 10.0, bottom: 8, top: 5),
          child: ClipRRect(
            borderRadius: BorderRadiusGeometry.circular(10),
            child: Image.asset(
              "assets/icons/Pomo_icon.png",
              fit: BoxFit.fitWidth,
            ),
          ),
        ),
        title: Text(
          "AgroX",
          style: GoogleFonts.moiraiOne(
            color: Colors.black,
            fontWeight: FontWeight.bold,
            fontSize: 25
          ),
        ),
        centerTitle: true,
      ),
      body: IndexedStack(index: curr_page_index, children: pages),
    );
  }
}
