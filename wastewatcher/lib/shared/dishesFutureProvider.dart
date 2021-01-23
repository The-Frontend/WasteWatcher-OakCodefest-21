import 'package:flutter_riverpod/all.dart';
import 'package:wastewatcher/models/dish.dart';
import 'package:wastewatcher/services/apiService.dart';

final dishesFutureProvider = FutureProvider.autoDispose<List<Dish>>(
  (ref) async {
    ref.maintainState = true;
    final apiService = ref.read(apiServiceProvider);
    final dishes = await apiService.getDishes();
    return dishes;
  },
);
