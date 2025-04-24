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
void solve() {
  ll d, sumTime;
  cin >> d >> sumTime;
  V<pint> limits(d);
  fori(0, d) {
    cin >> limits[i].ff >> limits[i].ss;
  }

  ll minTotal = 0, maxTotal = 0;
  for (auto &p : limits) {
    minTotal += p.ff;
    maxTotal += p.ss;
  }

  if (sumTime < minTotal || sumTime > maxTotal) {
    cout << "NO\n";
    return;
  }

  V<ll> schedule(d);
  fori(0, d) {
    schedule[i] = limits[i].ff;
  }

  ll remaining = sumTime - minTotal;
  fori(0, d) {
    if (remaining <= 0) break;
    ll possibleAdd = limits[i].ss - limits[i].ff;
    ll add = min(possibleAdd, remaining);
    schedule[i] += add;
    remaining -= add;
  }

  cout << "YES\n";
  cout << schedule edl;
}

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