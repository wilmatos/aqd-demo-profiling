# KCachegrind Usage Guide for Python Profiling

This guide explains how to use KCachegrind to analyze Python profiling data in the image processing project.

## Getting Started

KCachegrind has been set up in this project to visualize profiling data. You can run profiling and open KCachegrind in one step:

```bash
python -m profiling.run_profiling_with_visualization
```

## Understanding the KCachegrind Interface

When KCachegrind opens, you'll see several panels:

### 1. Main View (Top Right)

This shows the currently selected visualization. By default, it shows the "Call Graph" - a graphical representation of function calls. You can switch between different views using the tabs at the top:

- **Call Graph**: Visual representation of function calls
- **Treemap**: Shows relative time spent in functions as nested rectangles
- **Source Code**: Shows annotated source code when available
- **Machine Code**: Shows assembly code (not relevant for Python)

### 2. Function List (Top Left)

Lists all functions in your program, sorted by various metrics:

- **Incl.**: Inclusive cost (time spent in this function and all functions it calls)
- **Self**: Self cost (time spent only in this function, excluding calls)
- **Called**: Number of times the function was called
- **Function**: Function name

Click on any column header to sort by that metric.

### 3. Callers/Callees (Bottom)

Shows relationships between functions:

- **Callers**: Functions that call the selected function
- **Callees**: Functions called by the selected function

## Key Features to Use

### 1. Identifying Bottlenecks

1. Sort the function list by "Incl." to see which functions consume the most time
2. Look for functions with high "Self" time - these are direct bottlenecks
3. Pay attention to functions called many times - even if each call is fast

### 2. Analyzing Call Relationships

1. Select a function in the function list
2. Look at the "Callers" panel to see where it's called from
3. Look at the "Callees" panel to see what it calls
4. Use the call graph to visualize these relationships

### 3. Using the Treemap

The treemap provides a visual representation of where time is spent:

1. Click on the "Treemap" tab
2. Larger rectangles represent functions that consume more time
3. Nested rectangles show caller/callee relationships
4. Colors indicate different modules or libraries

### 4. Filtering and Focusing

To focus on specific parts of your code:

1. Right-click on a function and select "Go To"
2. Use the "Percentage" option in the toolbar to show relative costs
3. Use the search box to find specific functions

## Analyzing Our Image Processing Code

For our image processing application, pay special attention to:

### 1. Image Processing Operations

Look for PIL/Pillow operations that consume significant time:
- `gaussian_blur`
- `resize`
- `filter`
- `blend`

### 2. Inefficient Patterns

Identify patterns that suggest inefficiency:
- Multiple consecutive calls to the same function
- Excessive object creation (look for `copy` operations)
- Functions with high call counts

### 3. Optimization Targets

The best optimization targets are usually:
- Functions with high "Self" time
- Functions called many times
- Functions that could be parallelized

## Example Analysis

Here's an example analysis of our profiling data:

1. The `gaussian_blur` operation consumes the most self time
2. There are many calls to `Image.copy()` which create overhead
3. The `blend` operation is called frequently and consumes significant time
4. Processing is sequential, with no parallelism

## Next Steps

After identifying bottlenecks:

1. Use Amazon Q Developer to suggest optimizations
2. Implement changes to address the most significant bottlenecks
3. Run profiling again to measure improvements
4. Compare before/after results in KCachegrind

## Keyboard Shortcuts

- **Up/Down**: Navigate function list
- **Enter**: Select function and show details
- **Tab**: Cycle through panels
- **Ctrl+F**: Search for functions
- **F9**: Show/hide call graph

## Additional Resources

- [KCachegrind Documentation](https://kcachegrind.github.io/html/Documentation.html)
- [Valgrind Documentation](https://valgrind.org/docs/manual/cl-manual.html)
- [Python Profiling Documentation](https://docs.python.org/3/library/profile.html)