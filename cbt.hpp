#ifndef CBT_HPP
#define CBT_HPP

#include <bits/stdc++.h>
using namespace std;

struct Node {
    string label;
    unordered_map<char, Node*> children;
    vector<pair<string,int>> bucket;
    bool isEnd;

    Node(string l="") : label(l), isEnd(false) {}
};

class CBT {
private:
    Node* root;
    int BUCKET_THRESHOLD = 5;

    string toLower(string s);
    int lcp(string a, string b);

    void burst(Node* node);
    void collect(Node* node, string prefix,
                 vector<pair<string,int>>& res);

    int editDistance(string a, string b);

public:
    CBT();

    void insert(string word);
    bool search(string word);
    void remove(string word);

    vector<string> autocomplete(string prefix);
    vector<string> fuzzySearch(string word);

    void save(string filename);
    void load(string filename);
};

#endif