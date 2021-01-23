import 'package:flutter/material.dart';
import 'package:wastewatcher/models/dish.dart';

class DishContainer extends StatelessWidget {
  final Dish dish;
  const DishContainer({
    @required this.dish,
  });
  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: CircleAvatar(
          backgroundImage: NetworkImage(
            'eehee',
          ),
        ),
        title: Row(
          children: <Widget>[
            Column(
              children: dish.ingredients.map((ingredient) {
                return Text(
                  ingredient,
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }
}
