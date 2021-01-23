import 'package:flutter_riverpod/all.dart';
import 'package:flutter/material.dart';
import 'package:wastewatcher/components/dishContainer.dart';
import 'package:wastewatcher/constants/colors.dart';
import 'package:wastewatcher/models/dish.dart';
import 'package:wastewatcher/shared/dishesFutureProvider.dart';

final selectedDishStateProvider = StateProvider.autoDispose<Dish>((ref) {
  ref.maintainState = true;
  return null;
});

class DishListScreen extends ConsumerWidget {
  dynamic _refreshDishes(BuildContext context) {
    return context.refresh(dishesFutureProvider);
  }

  void _handleDishTileTap(BuildContext context, {@required Dish dish}) {
    context.read(selectedDishStateProvider).state = dish;
  }

  @override
  Widget build(BuildContext context, ScopedReader watch) {
    final selectedDish = watch(selectedDishStateProvider).state;
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
                itemCount: dishes.length + 1,
                itemBuilder: (context, index) {
                  if (index == 0) {
                    if (selectedDish != null) {
                      return Center(
                        child: DishContainer(
                          dish: selectedDish,
                        ),
                      );
                    } else {
                      return Container();
                    }
                  }
                  return Card(
                    child: ListTile(
                      onTap: () => _handleDishTileTap(
                        context,
                        dish: dishes[index - 1],
                      ),
                      title: Text(
                        dishes[index - 1].name,
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
