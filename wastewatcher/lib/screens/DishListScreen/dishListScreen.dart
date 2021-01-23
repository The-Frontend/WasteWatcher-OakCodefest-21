import 'package:flutter_riverpod/all.dart';
import 'package:flutter/material.dart';
import 'package:wastewatcher/components/dishCard.dart';
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
    _showDishCardDialog(context);
  }

  void _showDishCardDialog(BuildContext context) {
    final selectedDish = context.read(selectedDishStateProvider).state;
    showDialog(
      context: context,
      builder: (context) {
        return DishCard(
          dish: selectedDish,
        );
      },
    );
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
                      onTap: () => _handleDishTileTap(
                        context,
                        dish: dishes[index],
                      ),
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
