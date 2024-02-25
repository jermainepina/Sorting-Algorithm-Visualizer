import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
import random

# Bubble sort algorithm
def bubbleSort(a):
    n = len(a)
    for i in range(n):
        for j in range(0, n-1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                yield a

# Insertion sort algorithm
def insertionSort(a):
    for i in range(1, len(a)):
        j = i 
        while j > 0 and a[j] < a[j - 1]:
            a[j], a[j - 1] = a[j - 1], a[j]
            j -= 1
            yield a

# Merge sort algorithm
def mergeSort(arr, start, end):
    if end <= start:
        return
    mid = start + ((end - start + 1) // 2) - 1
    yield from mergeSort(arr, start, mid)
    yield from mergeSort(arr, mid + 1, end)
    yield from merge(arr, start, mid, end)
    yield arr
    
# Helper function for merge sort
def merge(a, start, mid, end):
    merged = []
    left_index = start
    right_index = mid + 1
    while left_index <= mid and right_index <= end:
        if a[left_index] < a[right_index]:
            merged.append(a[left_index])
            left_index += 1
        else:
            merged.append(a[right_index])
            right_index += 1
    merged += a[left_index:mid + 1]
    merged += a[right_index:end + 1]    
    for val in merged:
        a[start] = val
        start += 1
        yield a

# Quick sort algorithm
def quickSort(a, start, end):
    if end <= start: 
        return    
    pivot = a[end]
    pivot_index = start
    for i in range(start, end):
        if a[i] < pivot:
            a[i], a[pivot_index] = a[pivot_index], a[i]
            pivot_index += 1
        yield a
    a[end], a[pivot_index] = a[pivot_index], a[end]
    yield a
    yield from quickSort(a, start, pivot_index - 1)
    yield from quickSort(a, pivot_index + 1, end)
    
# Selection sort algorithm
def selectionSort(a):
    n = len(a)
    for i in range(n):
        min_index = i
 
        for j in range(i + 1, n):
            if a[j] < a[min_index]:
                min_index = j
                yield a
        (a[i], a[min_index]) = (a[min_index], a[i])
        yield a
        
# Shell sort algorithm
def shellSort(a):
    n = len(a)
    gap = n // 2
    while gap > 0:
        for i in range(gap,n):
            temp = a[i]
            j = i
            while j >= gap and a[j - gap] > temp:
                a[j] = a[j-gap]
                j -= gap
                yield a
            a[j] = temp
        gap //= 2
        yield a

def main():
    
    # User input for range of integers and sorting algorithm
    #   * List of specified length is shuffled randomly for sorting
    #   * User choses sorting method by inputing first letter of algorithm
    n = int(input("Enter number of integers to be sorted:\n"))
    a = random.sample(range(1, n + 1), n)
    algo = input("\nEnter sorting method:\nbubble: b\ninsertion: i\nmerge: m\nquick: q\nselection: se\nshell: sh\n")
    
    # Selects algorithm based off user input
    if algo == "b":
        title = "Bubble Sort\nAvg. Time Complexity: O(n^2)"
        generator = bubbleSort(a)
    elif algo == "i":
        title = "Insertion Sort\nAvg. Time Complexity: O(n^2)"
        generator = insertionSort(a)
    elif algo == "m":
        title = "Merge Sort\nAvg. Time Complexity: O(n*log(n))"
        generator = mergeSort(a, 0, n - 1)
    elif algo == "q":
        title = "Quick Sort\nAvg. Time Complexity: O(n*log(n))"
        generator = quickSort(a, 0, n - 1)
    elif algo == "se":
        title = "Selection Sort\nAvg. Time Complexity: O(n^2)"
        generator = selectionSort(a)
    elif algo == "sh":
        title = "Shell Sort\nAvg. Time Complexity: O(n*log(n)^2)"
        generator = shellSort(a)
    else:
        raise Exception("Incorrect letter provided")
    
    # Initialize figure, bar plot, axes/axes limits, title, color(s)
    # NOTE: Each bar represents an element in the list, with the X-axis representing its current index, and
    # the Y-axis representing the integer value of the element.
    plt.style.use('seaborn-v0_8-white')
    gradient_cmap = colors.LinearSegmentedColormap.from_list('custom_gradient', ['#6CB8E6', '#053958'])
    fig, ax = plt.subplots()
    ax.set_title(title)
    rects = ax.bar(range(len(a)), a, align="edge", color=gradient_cmap(range(len(a))))
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    
    # Text to represent live operation counter
    # (operations are determined by each yield returned by the sorting function)
    text = ax.text(0.01, 0.95, "", transform=ax.transAxes)
    
    # The "operations" variable represents the number of operations so far
    #   * The update() function increments operations[] and passes it to text label
    #   * Initialized to a list of one element so incrementation of variable is reflected outside the function 
    #     (lists are passed by reference).
    operations = [0]
    def update(a, rects):
        for rect, val in zip(rects, a):
            rect.set_height(val)
        operations[0] += 1
        text.set_text(f"Operations: {operations[0]}")
    
    # Function to animate sorting algorithm 
    # If a faster/slower animation speed is desired, adjust the "interval" variable.
    ani = animation.FuncAnimation(fig, func=update, fargs=(rects,), frames=generator, 
                                  interval=1, cache_frame_data=False, repeat=False)

    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__": 
    main()
