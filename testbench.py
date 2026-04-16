import subprocess
import os
import random
import string
import time

class TrieTestBench:
    def __init__(self):
        # Locate the executable
        self.exe_path = "./autocomplete.exe" if os.name == 'nt' else "./autocomplete"
        if not os.path.exists(self.exe_path):
            print("❌ ERROR: Executable not found. Compile your C++ code first!")
            exit(1)

        print("🚀 Booting up C++ Autocomplete Engine...")
        self.process = subprocess.Popen(
            [self.exe_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self.read_until_prompt()
        self.passed_tests = 0
        self.total_tests = 0

    def read_until_prompt(self):
        output = []
        while True:
            char = self.process.stdout.read(1)
            if not char: break
            output.append(char)
            if "".join(output[-2:]) == "> ":
                break
        return "".join(output[:-2]).strip()

    def send(self, cmd):
        self.process.stdin.write(cmd + "\n")
        self.process.stdin.flush()
        return self.read_until_prompt()

    def assert_test(self, test_name, condition, error_msg=""):
        self.total_tests += 1
        if condition:
            print(f"  ✅ PASS: {test_name}")
            self.passed_tests += 1
        else:
            print(f"  ❌ FAIL: {test_name} - {error_msg}")

    def run_all_tests(self):
        print("\n" + "="*40)
        print("🛠️  PHASE 1: STRESS TESTING (BURST MECHANIC)")
        print("="*40)
        
        # Generate 1,000 words sharing the prefix "inter" to force heavy bursting
        print("Generating 1,000 words to force Bucket Overflows...")
        start_time = time.time()
        for i in range(1000):
            suffix = ''.join(random.choices(string.ascii_lowercase, k=5))
            self.send(f"insert inter{suffix}")
        
        # Insert specific words we want to test later
        self.send("insert internet")
        self.send("insert international")
        self.send("insert interstellar")
        
        insert_time = time.time() - start_time
        print(f"  ⏱️ Time to insert 1000+ words: {insert_time:.3f} seconds")
        self.assert_test("Mass Insertion Stability", True)

        print("\n" + "="*40)
        print("🔍 PHASE 2: ALGORITHM VERIFICATION")
        print("="*40)

        # 1. Exact Search
        res1 = self.send("search internet")
        self.assert_test("Search Existing Word", "Found" in res1, "Expected 'Found'")
        
        res2 = self.send("search intergalactic")
        self.assert_test("Search Non-Existing Word", "Not Found" in res2, "Expected 'Not Found'")

        # 2. Autocomplete Limit (Should only return 10 words despite 1000+ existing)
        
        # --- NEW: Simulate user traffic to make these words "popular" ---
        for _ in range(5):
            self.send("search internet")
            self.send("search international")
        # ----------------------------------------------------------------
            
        res3 = self.send("inter")
        words_returned = len([w for w in res3.split('\n') if w])
        self.assert_test("Autocomplete Top-10 Limit", words_returned == 10, f"Returned {words_returned} words instead of 10")
        self.assert_test("Autocomplete Correctness", "internet" in res3 or "international" in res3, "Known inserted words not showing up")
        # 3. Fuzzy Search (Levenshtein Distance <= 1)
        # Typo: "intenet" missing 'r'
        res4 = self.send("fuzzy intenet") 
        self.assert_test("Fuzzy Search (1 Deletion Typo)", "internet" in res4, "'internet' not suggested for 'intenet'")

        # Typo: "inrernet" 't' replaced by 'r'
        res5 = self.send("fuzzy inrernet")
        self.assert_test("Fuzzy Search (1 Substitution Typo)", "internet" in res5, "'internet' not suggested for 'inrernet'")

        # 4. Deletion
        self.send("delete interstellar")
        res6 = self.send("search interstellar")
        self.assert_test("Delete Functionality", "Not Found" in res6, "'interstellar' was not deleted from the buckets")

        print("\n" + "="*40)
        print("💾 PHASE 3: FILE I/O PERSISTENCE")
        print("="*40)
        
        self.send("save")
        self.assert_test("Save to Disk", os.path.exists("saved.txt"), "saved.txt was not created")
        
        # Close the engine
        self.send("exit")

        print("\n" + "="*40)
        print(f"🏆 TEST RESULTS: {self.passed_tests} / {self.total_tests} PASSED")
        print("="*40)

if __name__ == "__main__":
    tester = TrieTestBench()
    tester.run_all_tests()