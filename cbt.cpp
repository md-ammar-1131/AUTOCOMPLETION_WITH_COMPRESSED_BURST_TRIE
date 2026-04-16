#include "cbt.hpp"

string CBT::toLower(string s) {
    for (auto &c : s) c = tolower(c);
    return s;
}

int CBT::lcp(string a, string b) {
    int i = 0;
    while (i < a.size() && i < b.size() && a[i] == b[i]) i++;
    return i;
}

CBT::CBT() {
    root = new Node();
}

// BURST
void CBT::burst(Node* node) {
    for (auto &p : node->bucket) {
        string word = p.first;
        int freq = p.second;

        if (word.empty()) continue;

        char c = word[0];
        if (!node->children[c])
            node->children[c] = new Node(string(1,c));

        node->children[c]->bucket.push_back({word.substr(1), freq});
    }
    node->bucket.clear();
}

// INSERT
void CBT::insert(string word) {
    word = toLower(word);
    Node* curr = root;
    string remaining = word;

    while (true) {
        bool moved = false;

        for (auto &it : curr->children) {
            Node* child = it.second;
            int len = lcp(child->label, remaining);

            if (len > 0) {
                if (len < child->label.size()) {
                    Node* split = new Node(child->label.substr(0,len));
                    child->label = child->label.substr(len);

                    split->children[child->label[0]] = child;
                    curr->children[split->label[0]] = split;
                    curr->children.erase(it.first);

                    curr = split;
                } else {
                    curr = child;
                }

                remaining = remaining.substr(len);
                moved = true;
                break;
            }
        }

        if (!moved) {
            curr->bucket.push_back({remaining,1});
            if (curr->bucket.size() > BUCKET_THRESHOLD)
                burst(curr);
            return;
        }

        if (remaining.empty()) {
            curr->isEnd = true;
            return;
        }
    }
}

// SEARCH + frequency update (Fixed)
bool CBT::search(string word) {
    word = toLower(word);
    Node* curr = root;
    string remaining = word;

    // 1. Traverse down the tree to find the node
    while (!remaining.empty()) {
        bool moved = false;

        for (auto &it : curr->children) {
            Node* child = it.second;
            int len = lcp(child->label, remaining);

            if (len == child->label.size()) {
                remaining = remaining.substr(len);
                curr = child;
                moved = true;
                break;
            }
        }
        if (!moved) break;
    }

    // 2. Look in the bucket, confirm it exists, and UPDATE frequency
    for (auto &p : curr->bucket) {
        if (p.first == remaining && p.second > 0) {
            p.second += 1;  // <--- THE MISSING "LEARNING" MECHANIC!
            return true;
        }
    }

    return false;
}
// DELETE
// DELETE 
void CBT::remove(string word) {
    word = toLower(word);
    Node* curr = root;
    string remaining = word;

    // 1. Walk down the tree to find where this word is stored
    while (!remaining.empty()) {
        bool moved = false;

        for (auto &it : curr->children) {
            Node* child = it.second;
            int len = lcp(child->label, remaining);

            if (len == child->label.size()) { 
                remaining = remaining.substr(len);
                curr = child;
                moved = true;
                break;
            }
        }
        if (!moved) break; // We found the correct node
    }

    // 2. Look inside this specific node's bucket and set frequency to 0
    for (auto &p : curr->bucket) {
        if (p.first == remaining) {
            p.second = 0; 
            return;
        }
    }
}

// COLLECT
void CBT::collect(Node* node, string prefix,
                  vector<pair<string,int>>& res) {

    for (auto &p : node->bucket)
        if (p.second > 0)
            res.push_back({prefix + p.first, p.second});

    for (auto &it : node->children) {
        Node* child = it.second;
        collect(child, prefix + child->label, res);
    }
}

// AUTOCOMPLETE
vector<string> CBT::autocomplete(string prefix) {
    prefix = toLower(prefix);
    Node* curr = root;
    string remaining = prefix;

    while (!remaining.empty()) {
        bool found = false;

        for (auto &it : curr->children) {
            Node* child = it.second;
            int len = lcp(child->label, remaining);

            if (len > 0) {
                curr = child;
                remaining = remaining.substr(len);
                found = true;
                break;
            }
        }
        if (!found) return {};
    }

    vector<pair<string,int>> temp;
    collect(curr, prefix, temp);

    sort(temp.begin(), temp.end(),
         [](auto &a, auto &b){
             if (a.second != b.second)
                 return a.second > b.second;
             return a.first < b.first;
         });

    vector<string> res;
    for (int i = 0; i < temp.size() && i < 10; i++)
        res.push_back(temp[i].first);

    return res;
}

// EDIT DISTANCE
int CBT::editDistance(string a, string b) {
    int n = a.size(), m = b.size();
    vector<vector<int>> dp(n+1, vector<int>(m+1));

    for (int i=0;i<=n;i++)
        for (int j=0;j<=m;j++) {
            if (i==0) dp[i][j]=j;
            else if (j==0) dp[i][j]=i;
            else if (a[i-1]==b[j-1])
                dp[i][j]=dp[i-1][j-1];
            else
                dp[i][j]=1+min({dp[i-1][j],
                                dp[i][j-1],
                                dp[i-1][j-1]});
        }
    return dp[n][m];
}

// FUZZY SEARCH
vector<string> CBT::fuzzySearch(string word) {
    vector<pair<string,int>> all;
    collect(root,"",all);

    vector<string> res;
    for (auto &p : all) {
        if (editDistance(word,p.first) <= 1)
            res.push_back(p.first);
    }
    return res;
}

// SAVE
void CBT::save(string filename) {
    ofstream out(filename);
    vector<pair<string,int>> all;
    collect(root,"",all);

    for (auto &p : all)
        out << p.first << " " << p.second << "\n";
}

// LOAD
void CBT::load(string filename) {
    ifstream in(filename);
    string w; int f;
    while (in >> w >> f) {
        insert(w);
    }
}