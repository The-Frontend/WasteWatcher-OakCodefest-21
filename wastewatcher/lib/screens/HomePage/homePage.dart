import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/all.dart';
import 'package:pie_chart/pie_chart.dart';
import 'package:wastewatcher/constants/colors.dart';
import 'package:wastewatcher/constants/routes.dart' as _routes;
import 'package:wastewatcher/shared/dishesFutureProvider.dart';
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
              Center(
                child: Column(
                  children: <Widget>[
                    Text(
                      '5.3',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 40.0,
                      ),
                    ),
                    Text(
                      'kilograms wasted',
                      style: TextStyle(
                        fontSize: 24.0,
                      ),
                    ),
                  ],
                ),
              ),
              // fl_chart.PieChart(
              //   fl_chart.PieChartData(
              //     sections: pieChartIngredientsDataMap.keys.map(
              //       (ingredientName) {
              //         final percentage =
              //             100 * pieChartIngredientsDataMap[ingredientName];
              //         return fl_chart.PieChartSectionData(
              //           title: '$percentage%',
              //           value: percentage,
              //         );
              //       },
              //     ).toList(),
              //     pieTouchData: fl_chart.PieTouchData(
              //       touchCallback: (fl_chart.PieTouchResponse touchResponse) {
              //         print('touched');
              //       },
              //     ),
              //   ),
              // ),
              PieChart(
                colorList: <Color>[
                  Colors.green[300],
                  Colors.green[600],
                  Colors.green[900],
                ],
                chartRadius: screenSize.width / 1.8,
                dataMap: getIngredientsMapFromDishes(dishes),
                chartLegendSpacing: screenSize.width / 36,
                legendOptions: LegendOptions(
                  legendPosition: LegendPosition.bottom,
                  showLegends: true,
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
          print(error);
          print(stackTrace);
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
