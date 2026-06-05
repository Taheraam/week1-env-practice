def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Finds the indices of two numbers in the list that add up to the target.
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    # 1. Initialize the hash map (dictionary)
    # Stores: { value_we_have_seen : index_where_we_saw_it }
    seen = {}
    
    # 2. Loop through the array tracking both index (i) and the number (num)
    for i, num in enumerate(nums):
        
        # 3. Calculate the required missing pair
        complement = target - num
        
        # 4. Check if we already encountered the complement earlier
        if complement in seen:
            # Found it! Return the previous index and current index
            return [seen[complement], i]
        
        # 5. If not found, log the current number and index into our dictionary
        seen[num] = i
        
    # Return an empty list if no solution is found (though the problem guarantees one)
    return []

# --- Test Cases ---
if __name__ == "__main__":
    # Example 1 (Your case)
    print("Example 1:", two_sum([2, 7, 11, 15], 9))  # Output: [0, 1]
    
    # Example 2 (Duplicates / Target is sum of same numbers)
    print("Example 2:", two_sum([3, 2, 4], 6))       # Output: [1, 2]
    
    # Example 3 (Identical values)
    print("Example 3:", two_sum([3, 3], 6))          # Output: [0, 1]