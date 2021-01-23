import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/all.dart';
import 'package:wastewatcher/router.dart' as _router;
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
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
    ]);
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomePage(),
      onGenerateRoute: _router.generateRoute,
    );
  }
}
