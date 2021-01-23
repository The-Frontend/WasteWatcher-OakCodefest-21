import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:wastewatcher/constants/routes.dart' as _routes;
import 'package:wastewatcher/screens/DishListScreen/dishListScreen.dart';

Route<dynamic> generateRoute(RouteSettings settings) {
  switch (settings.name) {
    case _routes.dishListScreenRoute:
      return MaterialPageRoute(
        builder: (context) => DishListScreen(),
      );
    default:
      return null;
  }
}
