import 'package:agrox/tools/colorTheme.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class Homepage extends StatefulWidget {
  final String username;
  const Homepage({super.key, required this.username});

  @override
  State<Homepage> createState() => _HomepageState();
}

class _HomepageState extends State<Homepage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.only(top: 25, left: 25, bottom: 0),
              child: Container(
                child: Align(
                  alignment: AlignmentGeometry.topLeft,
                  child: Text(
                    "Hello, ${widget.username} !",
                    style: GoogleFonts.dancingScript(
                      fontSize: 30,
                      fontWeight: FontWeight.w700,
                      color: kAccentVariant,
                    ),
                  ),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(10.0),
              child: Container(
                height: 150,
                width: double.infinity,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(20),
                  color: const Color.fromARGB(223, 82, 179, 208),
                ),
                child: Row(
                  children: [
                    Container(
                      width: 250,
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Center(
                            child: Text(
                              "Today's Weather",
                              style: GoogleFonts.josefinSans(fontSize: 15),
                            ),
                          ),
                          Center(
                            child: Text(
                              "Sunny 32 ℃",
                              style: GoogleFonts.josefinSans(fontSize: 30),
                            ),
                          ),
                        ],
                      ),
                    ),
                    Icon(
                      Icons.sunny,
                      size: 60,
                      color: const Color.fromARGB(255, 248, 209, 90),
                    ),
                  ],
                ),
              ),
            ),
            Align(
              alignment: Alignment.bottomLeft,
              child: Padding(
                padding: const EdgeInsets.all(10.0),
                child: Container(
                  height: 175,
                  width: double.infinity,
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.black),
                    color: const Color.fromARGB(206, 190, 248, 254),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Column(
                    children: [
                      Padding(
                        padding: const EdgeInsets.only(left: 17.0, top: 13),
                        child: Align(
                          alignment: Alignment.topLeft,
                          child: Text(
                            "AI-Powered Crop Care",
                            style: TextStyle(fontSize: 12),
                          ),
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.only(left: 17.0, top: 5),
                        child: Align(
                          alignment: Alignment.topLeft,
                          child: Text(
                            "Check your Pomogrenate's health",
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.only(left: 17.0, top: 3),
                        child: Align(
                          alignment: Alignment.topLeft,
                          child: Row(
                            children: [
                              Text(
                                "Scan a fruit to diagnose.",
                                style: TextStyle(fontSize: 13),
                              ),
                              SizedBox(width: 100),
                              Icon(
                                Icons.document_scanner_outlined,
                                size: 40,
                                color: Colors.white,
                              ),
                            ],
                          ),
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Center(
                          child: ElevatedButton(
                            style: ElevatedButton.styleFrom(
                              backgroundColor: const Color.fromARGB(
                                255,
                                25,
                                149,
                                154,
                              ),
                              shadowColor: Colors.white,
                              fixedSize: Size(double.maxFinite, 40),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadiusGeometry.circular(16),
                              ),
                              elevation: 10,
                            ),
                            onPressed: () {},
                            child: Center(
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(
                                    Icons.camera_alt,
                                    size: 25,
                                    color: const Color.fromARGB(
                                      255,
                                      250,
                                      250,
                                      250,
                                    ),
                                  ),
                                  SizedBox(width: 10),
                                  Text(
                                    "Scan a fruit",
                                    style: TextStyle(
                                      color: const Color.fromARGB(
                                        255,
                                        255,
                                        255,
                                        255,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Container(
                    height: 130,
                    width: 170,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(20),
                      color: kMint,
                    ),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(decoration: BoxDecoration(color: Colors.white,borderRadius: BorderRadius.circular(10)),child: Padding(
                          padding: const EdgeInsets.all(5.0),
                          child: Icon(Icons.shopping_cart,size: 40,),
                        )),
                        Padding(
                          padding: const EdgeInsets.all(5.0),
                          child: Text("Market Prices"),
                        )
                      ],
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Container(
                    height: 130,
                    width: 170,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(20),
                      color: kMint,
                    ),
                  ),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Container(
                    height: 130,
                    width: 170,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(20),
                      color: kMint,
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Container(
                    height: 130,
                    width: 170,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(20),
                      color: kMint,
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
