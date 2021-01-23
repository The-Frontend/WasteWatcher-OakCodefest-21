import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/all.dart';
import 'package:pie_chart/pie_chart.dart';
import 'package:wastewatcher/constants/colors.dart';
import 'package:wastewatcher/constants/routes.dart' as _routes;
import 'package:wastewatcher/shared/dishesProvider.dart';
import 'package:wastewatcher/utilities.dart';

class HomePage extends ConsumerWidget {
  Future<void> _navigateToDishListScreen(BuildContext context) async {
    await Navigator.pushNamed(context, _routes.dishListScreenRoute);
  }

  @override
  Widget build(BuildContext context, ScopedReader watch) {
    Size screenSize = MediaQuery.of(context).size;
    return Scaffold(
      appBar: AppBar(
        backgroundColor: appBarColor,
        title: Text(
          'WasteWatcher',
        ),
        centerTitle: true,
      ),
      body: watch(dishesFutureProvider).when<Widget>(
        data: (dishes) {
          return Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              Text(
                'X Kgs Wasted',
                style: TextStyle(
                  color: Colors.grey[700],
                  fontSize: 20.0,
                ),
              ),
              PieChart(
                chartRadius: screenSize.width / 1.8,
                dataMap: getIngredientsMapFromDishes(dishes),
                chartLegendSpacing: screenSize.width / 36,
                legendOptions: LegendOptions(
                  legendPosition: LegendPosition.top,
                ),
                chartValuesOptions: ChartValuesOptions(
                  showChartValuesInPercentage: true,
                ),
              ),
              MaterialButton(
                onPressed: () => _navigateToDishListScreen(context),
                elevation: 2.0,
                color: appBarColor,
                child: Icon(
                  Icons.keyboard_arrow_right_outlined,
                  size: 20.0,
                ),
                padding: EdgeInsets.all(
                  15.0,
                ),
                shape: CircleBorder(),
              ),
            ],
          );
        },
        loading: () => Center(
          child: CircularProgressIndicator(),
        ),
        error: (error, stackTrace) {
          return Center(
            child: Text(
              'Something went wrong...',
            ),
          );
        },
      ),
    );
  }
}
