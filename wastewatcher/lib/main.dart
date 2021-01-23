import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:wastewatcher/screens/HomePage/homePage.dart';

void main() {
  runApp(
    ProviderScope(
      child: RootWidget(),
    ),
  );
}

class RootWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: HomePage(),
    );
  }
}
