#include "cbt.hpp"

int main() {
    CBT trie;

    // load initial data
    ifstream file("data.txt");
    string word;
    while (file >> word)
        trie.insert(word);

    cout << "=== AUTOCOMPLETE ENGINE ===\n";

    string cmd;
    while (true) {
        // flush is critical here for Python to read the prompt!
        cout << "\n> " << flush; 
        getline(cin, cmd);

        if (cmd == "exit") break;

        if (cmd.find("search ") == 0) {
            string w = cmd.substr(7);
            cout << (trie.search(w) ? "Found\n" : "Not Found\n");
        }
        else if (cmd.find("insert ") == 0) {
            string w = cmd.substr(7);
            trie.insert(w);
            cout << "Inserted\n";
        }
        else if (cmd.find("delete ") == 0) {
            string w = cmd.substr(7);
            trie.remove(w);
            cout << "Deleted\n";
        }
        else if (cmd.find("fuzzy ") == 0) {
            string w = cmd.substr(6);
            auto res = trie.fuzzySearch(w);
            for (auto &s : res) cout << s << endl;
        }
        else if (cmd == "save") {
            trie.save("saved.txt");
            cout << "Saved\n";
        }
        else {
            auto res = trie.autocomplete(cmd);
            for (auto &s : res) cout << s << endl;
        }
    }
}