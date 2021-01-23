import 'package:meta/meta.dart';
import 'package:wastewatcher/models/dish.dart';
import 'package:intl/intl.dart';

Map<String, double> getIngredientsMapFromDishes(@required List<Dish> dishes) {
  Map<String, double> ingredientsMap = {};
  for (int i = 0; i < dishes.length; i++) {
    var dish = dishes[i];
    for (int j = 0; j < dish.ingredients.length; j++) {
      var ingredient = dish.ingredients[j];
      if (ingredientsMap.keys.contains(ingredient)) {
        ingredientsMap[ingredient] += dish.quantity;
      } else {
        ingredientsMap[ingredient] = dish.quantity.toDouble();
      }
    }
  }
  return ingredientsMap;
}

String dateTimeToString(DateTime dateTime) {
  return DateFormat('yyyy/MM/dd').format(dateTime);
}
