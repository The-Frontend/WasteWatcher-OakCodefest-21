import 'package:flutter_riverpod/all.dart';
import 'package:wastewatcher/models/dish.dart';

final apiServiceProvider = Provider<APIService>((ref) {
  return APIService();
});

class APIService {
  Future<List<Dish>> getDishes() async {
    await Future.delayed(
      Duration(
        seconds: 1,
      ),
    );
    var dishesJson = [
      {
        "name": "chocolate cake",
        "ingredients": ["cocoa", "bread"],
        "quantity": 5.0,
      },
    ];
    return dishesJson.map((dishJson) => Dish.fromMap(dishJson)).toList();
  }
}
