import 'package:flutter/material.dart';
import 'package:flutter_riverpod/all.dart';
import 'package:pie_chart/pie_chart.dart';
import 'package:wastewatcher/shared/dishesFutureProvider.dart';
import 'package:wastewatcher/shared/userProvider.dart';
import 'package:wastewatcher/utilities.dart';

class LandingPage extends ConsumerWidget {
  dynamic _refreshDishes(BuildContext context) {
    return context.refresh(dishesFutureProvider);
  }

  @override
  Widget build(BuildContext context, ScopedReader watch) {
    final screenSize = MediaQuery.of(context).size;
    final user = watch(userProvider);
    return watch(dishesFutureProvider).when<Widget>(
      data: (dishes) {
        return Container(
          decoration: BoxDecoration(
            image: DecorationImage(
              image: AssetImage(
                'images/appBackground.png',
              ),
              fit: BoxFit.cover,
            ),
          ),
          child: RefreshIndicator(
            child: ListView(
              children: <Widget>[
                SizedBox(
                  height: screenSize.height / 36,
                ),
                Center(
                  child: Container(
                    child: Column(
                      children: <Widget>[
                        Text(
                          user.massWasted.toString(),
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
                ),
                SizedBox(
                  height: screenSize.height / 36,
                ),
                PieChart(
                  colorList: <Color>[
                    Colors.green[300],
                    Colors.green[600],
                    Colors.green[900],
                  ],
                  chartRadius: screenSize.width / 1.8,
                  dataMap: getIngredientsMapFromDishes(
                    dishes: dishes,
                  ),
                  chartLegendSpacing: screenSize.width / 36,
                  legendOptions: LegendOptions(
                    legendPosition: LegendPosition.bottom,
                    showLegends: true,
                  ),
                  chartValuesOptions: ChartValuesOptions(
                    showChartValuesInPercentage: true,
                  ),
                ),
                SizedBox(
                  height: screenSize.height / 9,
                ),
              ],
            ),
            onRefresh: () => _refreshDishes(context),
          ),
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
    );
  }
}
