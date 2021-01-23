import 'package:flutter_riverpod/all.dart';
import 'package:http/http.dart' as http;
import 'package:wastewatcher/models/dish.dart';
import 'package:wastewatcher/models/edamamApiResponse.dart';
import 'package:meta/meta.dart';
import 'dart:convert';

final apiServiceProvider = Provider<APIService>((ref) {
  return APIService();
});

class APIService {
  static const API_BASE_URL = 'https://312b16c6e903.ngrok.io';

  Future<EdamamApiResponse> searchEdamamDishes({@required String query}) async {
    final response = await http.get(
      '$API_BASE_URL/dish-search/?query=$query',
    );
    return EdamamApiResponse.fromMap(
      json.decode(
        response.body,
      ),
    );
  }

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
      {
        "name": "pizza",
        "ingredients": ["cheese", "bread"],
        "quantity": 3.0,
      },
    ];
    return dishesJson.map((dishJson) => Dish.fromMap(dishJson)).toList();
  }
}
