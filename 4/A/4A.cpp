#include <bits/stdc++.h>

using namespace std;
using ll = long long;
template <typename T> using V = vector<T>;

#define fast_io                                                                \
  ios_base::sync_with_stdio(false);                                            \
  cin.tie(nullptr);                                                            \
  cout.tie(nullptr)
#define YN(condition) cout << ((condition) ? "YES" : "NO")
#define fori(s, e) for (ll i = s; i < e; i++)
#define edl << '\n'
#define sp << ' ' <<
#define all(a) a.begin(), a.end()
#define rall(a) a.rbegin(), a.rend()
#define ff first
#define ss second
#define pint pair<ll, ll>

template <typename T> using V = vector<T>;

// Helpful overloads for debugging bad code
// PAIR I/O

ostream &operator<<(ostream &ostr, const pint &x) {
  ostr << '{' << x.ff << ',' << x.ss << '}' << ' ';
  return ostr;
}

// VECTOR I/O overload

template <typename T> istream &operator>>(istream &istr, V<T> &v) {
  for (ll i = 0; i < v.size(); i++)
    istr >> v[i];
  return istr;
}

template <typename T> ostream &operator<<(ostream &ostr, const V<T> &v) {
  for (ll i = 0; i < v.size(); i++) {
    ostr << v[i] << ' ';
  }
  return ostr;
}

// SOLVE FUNCTION
void solve() {}

int main() {
  fast_io;

  ll t = 1;
  // use this snippet for multiline tests
  // std::cin >> t;
  while (t--) {
    solve();
  }
  return 0;
}