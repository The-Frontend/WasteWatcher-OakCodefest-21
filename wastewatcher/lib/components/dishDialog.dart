import 'package:flutter/material.dart';
import 'package:flutter_riverpod/all.dart';
import 'package:transparent_image/transparent_image.dart' as transparent_image;
import 'package:wastewatcher/models/dish.dart';
import 'package:wastewatcher/models/edamamApiResponse.dart';
import 'package:wastewatcher/shared/edamamApiResponseFutureProvider.dart';

class DishDialog extends ConsumerWidget {
  final Dish dish;
  const DishDialog({
    @required this.dish,
  });
  @override
  Widget build(BuildContext context, ScopedReader watch) {
    return AlertDialog(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadiusDirectional.circular(
          24.0,
        ),
      ),
      content: watch(
        edamamApiResponseFutureProvider(
          dish.dishName,
        ),
      ).when(
        data: (EdamamApiResponse edamamApiResponse) {
          return Center(
            child: ListView.builder(
              itemCount:
                  edamamApiResponse.hits[0].recipe.ingredientLines.length + 1,
              itemBuilder: (context, index) {
                if (index == 0) {
                  return Column(
                    children: <Widget>[
                      Container(
                        height: 150.0,
                        width: 150.0,
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(
                            24.0,
                          ),
                          child: FadeInImage.memoryNetwork(
                            placeholder: transparent_image.kTransparentImage,
                            image: edamamApiResponse.hits[0].recipe.image,
                          ),
                        ),
                        decoration: BoxDecoration(
                          shape: BoxShape.rectangle,
                        ),
                      ),
                      SizedBox(
                        height: 10.0,
                      ),
                      Text(
                        dish.dishName,
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 27.0,
                        ),
                      ),
                    ],
                  );
                } else {
                  return Text(
                    edamamApiResponse.hits[0].recipe.ingredientLines[index - 1],
                  );
                }
              },
            ),
          );
        },
        loading: () => Center(
          child: CircularProgressIndicator(),
        ),
        error: (error, stackTrace) {
          return Center(
            child: Icon(
              Icons.perm_scan_wifi,
              color: Colors.red,
            ),
          );
        },
      ),
    );
  }
}
