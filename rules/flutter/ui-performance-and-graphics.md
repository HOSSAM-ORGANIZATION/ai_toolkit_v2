## Agent card

**LOADMAP tags:** `perf`, `math`, `ui`
**Read rest of this file:** no — this card contains the full enforceable rule.

### Must
- Document every mathematical formula, coordinate transformation, and trigonometry operation step-by-step in `CustomPainter` or animation code.
- Prevent memory leaks: strictly dispose all `AnimationController`, `TickerProvider`, `ScrollController`, `TextEditingController`, and `StreamSubscription` instances in `State.dispose()`.
- Wrap animated or repainting subtrees in a `RepaintBoundary` to isolate their rasterization layer from static parent widgets.
- Instantiate `Paint` and `Path` objects as class members or cache them; never allocate new `Paint()` or `Path()` objects inside the `paint(Canvas canvas, Size size)` hot loop.
- Override `shouldRepaint` accurately in `CustomPainter`: return `false` if properties have not changed.
- **Simplicity First:** Always evaluate if built-in Flutter widgets (`AnimatedContainer`, `Transform`, `ClipRRect`, `DecoratedBox`) can achieve the UI goal before jumping to manual `CustomPaint` or matrix math.

### Must not
- Instantiate `Paint()` inside `CustomPainter.paint()`.
- Leave listeners attached to controllers after widget disposal.
- Animate widgets without `RepaintBoundary` when they share a screen with complex static layouts.
- Use `CustomPaint` or raw trigonometric equations without commenting the geometric purpose of each point and control point.

### When to load the rest
- Only when authoring high-complexity Canvas graphics, custom graphs, or specialized procedural shaders.

### Related (cards first)
- `+ui` for composition; `+clean-code` for architectural clarity.

# High-Performance UI, Memory Management & Graphics Transparency

## Purpose
Guarantees 60/120 FPS jank-free rendering, complete freedom from memory leaks, and crystal-clear mathematical documentation for any custom Canvas drawings or physics animations.

## 1. Memory Management & Lifecycle Checklist

Every stateful component managing resources must implement a clean `dispose()`:

```dart
class _AnimatedGaugeState extends State<AnimatedGauge> with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final ScrollController _scrollController;
  StreamSubscription<int>? _subscription;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: const Duration(milliseconds: 600));
    _scrollController = ScrollController();
    _subscription = widget.stream.listen((val) { /* handle */ });
  }

  @override
  void dispose() {
    // 1. Cancel streams first
    _subscription?.cancel();
    // 2. Dispose controllers
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }
}
```

## 2. Mathematical Transparency in CustomPaint

When implementing a `CustomPainter`, every geometric coordinate and calculation must be explicitly documented so any engineer can verify its correctness:

```dart
class ConcaveCardPainter extends CustomPainter {
  final Color color;
  final double curveDepth;

  // Cache Paint instance to avoid allocations during rasterization
  late final Paint _paint = Paint()
    ..color = color
    ..style = PaintingStyle.fill;

  ConcaveCardPainter({required this.color, required this.curveDepth});

  @override
  void paint(Canvas canvas, Size size) {
    final path = Path();
    final w = size.width;
    final h = size.height;

    // Start at top-left origin (0, 0)
    path.moveTo(0, 0);

    // Calculate midpoint for concave dip
    final midX = w / 2;
    // Control point pulls the quadratic bezier curve down by curveDepth
    path.quadraticBezierTo(midX, curveDepth, w, 0);

    // Draw straight perimeter to bottom-right, bottom-left, and close
    path.lineTo(w, h);
    path.lineTo(0, h);
    path.close();

    canvas.drawPath(path, _paint);
  }

  @override
  bool shouldRepaint(covariant ConcaveCardPainter oldDelegate) {
    return oldDelegate.color != color || oldDelegate.curveDepth != curveDepth;
  }
}
```

## 3. Repaint Boundaries for Heavy Animations
Always isolate animated widgets to avoid triggering a repaint cascade across the entire widget tree:

```dart
RepaintBoundary(
  child: AnimatedBuilder(
    animation: _controller,
    builder: (context, child) => CustomPaint(
      painter: RadarSweepPainter(_controller.value),
    ),
  ),
)
```
