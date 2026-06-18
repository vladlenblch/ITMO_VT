#include <iostream>
#include <map>
#include <string>

struct Node {
  std::map<std::string, Node*> children;
};

void create_new_folder(Node* curr, std::string folder_name) {
  if (!curr->children.contains(folder_name)) {
    curr->children[folder_name] = new Node();
  }
}

void print_tree(Node* node, int depth) {
  for (const auto& [name, child] : node->children) {
    std::cout << std::string(depth, ' ') << name << std::endl;
    print_tree(child, depth + 1);
  }
}

int main() {
  int folders_count;
  std::cin >> folders_count;

  Node* root = new Node();
  for (int i = 0; i < folders_count; i++) {
    std::string path;
    std::cin >> path;

    Node* curr = root;
    std::string folder_name;
    for (char ch : path) {
      if (ch == '\\') {
        create_new_folder(curr, folder_name);

        curr = curr->children[folder_name];
        folder_name.clear();
      } else {
        folder_name += ch;
      }
    }
    create_new_folder(curr, folder_name);
  }
  print_tree(root, 0);
}
