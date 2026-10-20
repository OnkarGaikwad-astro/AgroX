import 'package:agrox/homePage.dart';
import 'package:agrox/rootpage.dart';
import 'package:agrox/tools/colorTheme.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

void main() {
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        useMaterial3: true,
        textTheme: GoogleFonts.josefinSansTextTheme(
          Theme.of(context).textTheme,
        ),
        scaffoldBackgroundColor: kBackground
      ),
      debugShowCheckedModeBanner: false,
      home:Rootpage(username:"Onkar")
    );
  }
}
