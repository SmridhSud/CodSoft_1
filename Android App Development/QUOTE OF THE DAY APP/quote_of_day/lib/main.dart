import 'dart:math';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:share_plus/share_plus.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const QuoteApp());
}

class QuoteApp extends StatelessWidget {
  const QuoteApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Quote of the Day',
      home: QuoteHome(),
    );
  }
}

class QuoteHome extends StatefulWidget {
  const QuoteHome({Key? key}) : super(key: key);

  @override
  State<QuoteHome> createState() => _QuoteHomeState();
}

class _QuoteHomeState extends State<QuoteHome> {
  final List<String> _quotes = [
    "The best way to predict the future is to create it.",
    "Do one thing every day that scares you.",
    "Success is not final; failure is not fatal: It is the courage to continue that counts.",
    "Believe you can and you're halfway there.",
    "Small steps every day lead to big results.",
    "Be the change you want to see."
  ];

  String _current = '';
  List<String> _favorites = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _initStateAsync();
  }

  Future<void> _initStateAsync() async {
    await _loadQuote();
    setState(() => _loading = false);
  }

  Future<void> _loadQuote() async {
    final prefs = await SharedPreferences.getInstance();
    final storedDate = prefs.getString('lastDate');
    final today = DateTime.now().toIso8601String().split('T')[0];

    if (storedDate == today && prefs.containsKey('lastQuote')) {
      _current = prefs.getString('lastQuote') ?? _quotes.first;
    } else {
      final random = Random();
      _current = _quotes[random.nextInt(_quotes.length)];
      await prefs.setString('lastDate', today);
      await prefs.setString('lastQuote', _current);
    }

    _favorites = prefs.getStringList('favorites') ?? [];
  }

  Future<void> _toggleFavorite() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      if (_favorites.contains(_current)) {
        _favorites.remove(_current);
      } else {
        _favorites.add(_current);
      }
    });
    await prefs.setStringList('favorites', _favorites);
  }

  Future<void> _refreshQuote() async {
    final prefs = await SharedPreferences.getInstance();
    final random = Random();
    _current = _quotes[random.nextInt(_quotes.length)];
    final today = DateTime.now().toIso8601String().split('T')[0];
    await prefs.setString('lastDate', today);
    await prefs.setString('lastQuote', _current);
    setState(() {});
  }

  void _shareQuote() {
    if (_current.isNotEmpty) {
      Share.share(_current);
    }
  }

  @override
  Widget build(BuildContext context) {
    final isFav = _favorites.contains(_current);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Quote of the Day'),
        actions: [
          IconButton(
            icon: const Icon(Icons.favorite),
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute(builder: (_) => FavoritesScreen(favs: _favorites)),
            ),
            tooltip: 'Favorites',
          )
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Card(
              elevation: 6,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Text(
                  _current.isEmpty ? 'No quote available.' : '"$_current"',
                  textAlign: TextAlign.center,
                  style: const TextStyle(fontSize: 20, fontStyle: FontStyle.italic),
                ),
              ),
            ),
            const SizedBox(height: 24),
            Wrap(
              spacing: 12,
              alignment: WrapAlignment.center,
              children: [
                ElevatedButton.icon(
                  icon: const Icon(Icons.share),
                  label: const Text('Share'),
                  onPressed: _shareQuote,
                ),
                ElevatedButton.icon(
                  icon: Icon(isFav ? Icons.favorite : Icons.favorite_border),
                  label: Text(isFav ? 'Unfavorite' : 'Favorite'),
                  onPressed: _toggleFavorite,
                ),
                OutlinedButton.icon(
                  icon: const Icon(Icons.refresh),
                  label: const Text('Refresh'),
                  onPressed: _refreshQuote,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class FavoritesScreen extends StatelessWidget {
  final List<String> favs;
  const FavoritesScreen({Key? key, required this.favs}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Favorites')),
      body: favs.isEmpty
          ? const Center(child: Text('No favorites yet'))
          : ListView.separated(
        padding: const EdgeInsets.all(12),
        itemCount: favs.length,
        separatorBuilder: (_, __) => const Divider(),
        itemBuilder: (context, index) => ListTile(
          leading: const Icon(Icons.format_quote),
          title: Text(favs[index]),
          onLongPress: () async {
            final prefs = await SharedPreferences.getInstance();
            final newList = List<String>.from(favs)..removeAt(index);
            await prefs.setStringList('favorites', newList);
            Navigator.of(context).pop();
            Navigator.of(context).push(MaterialPageRoute(builder: (_) => FavoritesScreen(favs: newList)));
          },
        ),
      ),
    );
  }
}
