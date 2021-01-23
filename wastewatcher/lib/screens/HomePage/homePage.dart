import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/all.dart';
import 'package:pie_chart/pie_chart.dart';
import 'package:wastewatcher/constants/colors.dart';
import 'package:wastewatcher/shared/dishesProvider.dart';
import 'package:wastewatcher/utilities.dart';

class HomePage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, ScopedReader watch) {
    Size screenSize = MediaQuery.of(context).size;
    // print('width is: ${screenSize.width} and height is: ${screenSize.height}');
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
              Row(
                children: <Widget>[
                  PieChart(
                    chartRadius: screenSize.width / 3.5,
                    dataMap: getIngredientsMapFromDishes(dishes),
                    chartLegendSpacing: screenSize.width / 36,
                    legendOptions: LegendOptions(
                      legendPosition: LegendPosition.left,
                    ),
                    chartValuesOptions: ChartValuesOptions(
                      showChartValuesInPercentage: true,
                    ),
                  ),
                  SizedBox(
                    width: screenSize.width / 148,
                  ),
                  Column(
                    children: <Widget>[
                      SizedBox(
                        height: 100.0,
                      ),
                      MaterialButton(
                        onPressed: () {},
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
                  ),
                ],
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
