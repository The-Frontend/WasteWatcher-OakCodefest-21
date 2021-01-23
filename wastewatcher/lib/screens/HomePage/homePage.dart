import 'package:flutter/material.dart';
import 'package:flutter_riverpod/all.dart';
import 'package:wastewatcher/constants/colors.dart';
import 'package:wastewatcher/screens/DishListScreen/dishListScreen.dart';
import 'package:wastewatcher/screens/LandingPage/landingPage.dart';

final bottomNavigationIndexStateProvider =
    StateProvider.autoDispose<int>((ref) {
  return 0;
});

class HomePage extends ConsumerWidget {
  List<Widget> get bodyWidgets {
    return [
      LandingPage(),
      DishListScreen(),
    ];
  }

  @override
  Widget build(BuildContext context, ScopedReader watch) {
    final bottomNavigationIndex =
        watch(bottomNavigationIndexStateProvider).state;
    return Scaffold(
      appBar: AppBar(
        backgroundColor: appBarColor,
        title: Text(
          'WasteWatcher',
        ),
        centerTitle: true,
      ),
      body: bodyWidgets[bottomNavigationIndex],
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: Colors.green,
        selectedItemColor: Colors.white,
        currentIndex: bottomNavigationIndex,
        onTap: (int index) {
          context.read(bottomNavigationIndexStateProvider).state = index;
        },
        items: <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(
              Icons.home,
            ),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(
              Icons.emoji_food_beverage_outlined,
            ),
            label: 'Wasted Food',
          ),
        ],
      ),
    );
  }
}
