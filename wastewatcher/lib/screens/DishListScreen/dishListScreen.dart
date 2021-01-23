import 'package:flutter_riverpod/all.dart';
import 'package:flutter/material.dart';
import 'package:wastewatcher/components/dishDialog.dart';
import 'package:wastewatcher/constants/colors.dart';
import 'package:wastewatcher/models/dish.dart';
import 'package:wastewatcher/shared/dishesFutureProvider.dart';
import 'package:wastewatcher/utilities.dart';

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
        return DishDialog(
          dish: selectedDish,
        );
      },
    );
  }

  @override
  Widget build(BuildContext context, ScopedReader watch) {
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
                      trailing: IconButton(
                        onPressed: () => _handleDishTileTap(
                          context,
                          dish: dishes[index],
                        ),
                        icon: Icon(
                          Icons.more_horiz,
                        ),
                      ),
                      title: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: <Widget>[
                          Text(
                            dateTimeToString(
                              dishes[index].createdTimestamp,
                            ),
                          ),
                          Text(
                            dishes[index].dishName,
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
            onRefresh: () => _refreshDishes(context),
          ),
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
    );
  }
}
