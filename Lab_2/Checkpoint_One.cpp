/*
             CodEcstasy
            SUST SWE-19
*/
#include <bits/stdc++.h>
#define ll long long
#define s second
#define f first
#define fora(i,n) for(int i=0 ; i<n ; i++)
#define ford(i,n) for(int i=n-1 ; i>=0 ; i--)
#define b begin
#define e end
#define all(v) (v).begin(),(v).end()
#define pb push_back
using namespace std;

int main()
{
    string ciphertext;
    cout << "Enter the ciphertext: ";
    cin >> ciphertext;

    for (int shift = 0; shift < 26; shift++)
    {
        string plaintext = ciphertext;

        for (int i = 0; i < plaintext.size(); i++)
        {
            int char_index = plaintext[i] - 'a';
            char_index = (char_index + shift) % 26;
            plaintext[i] = char_index + 'a';
        }

        cout << "Shift " << shift << ": " << plaintext << endl;
    }

    return 0;
}
