import 'package:flutter_riverpod/all.dart';
import 'package:flutter/material.dart';
import 'package:wastewatcher/constants/colors.dart';
import 'package:wastewatcher/shared/dishesProvider.dart';

class DishListScreen extends ConsumerWidget {
  dynamic _refreshDishes(BuildContext context) {
    return context.refresh(dishesFutureProvider);
  }

  @override
  Widget build(BuildContext context, ScopedReader watch) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Wasted Dishes',
        ),
        backgroundColor: appBarColor,
      ),
      body: watch(dishesFutureProvider).when<Widget>(
        data: (dishes) {
          return RefreshIndicator(
            child: Center(
              child: ListView.builder(
                itemCount: dishes.length,
                itemBuilder: (context, index) {
                  return Card(
                    child: ListTile(
                      title: Text(
                        dishes[index].name,
                      ),
                    ),
                  );
                },
              ),
            ),
            onRefresh: () => _refreshDishes(context),
          );
        },
        loading: () => Center(
          child: CircularProgressIndicator(),
        ),
        error: (error, stackTrace) {
          return Text(
            error.toString(),
          );
        },
      ),
    );
  }
}
