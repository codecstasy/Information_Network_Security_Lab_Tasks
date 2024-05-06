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
    vector<pair<double, int>> frequencies{{8.05, 0}, {1.67, 1}, {2.23, 2}, {5.10, 3}, {12.22, 4}, {2.14, 5}, {2.30, 6}, {6.62, 7}, {6.28, 8}, {0.19, 9}, {0.95, 10}, {4.08, 11}, {2.33, 12}, {6.95, 13}, {7.63, 14}, {1.66, 15}, {0.06, 16}, {5.29, 17}, {6.02, 18}, {9.67, 19}, {2.92, 20}, {0.82, 21}, {2.60, 22}, {0.11, 23}, {2.04, 24}, {0.06, 25}};
    sort(frequencies.rbegin(), frequencies.rend());
    string ciphertext;
    string chunk;
    while (cin >> chunk)
    {
        ciphertext += chunk + " ";
    }
    vector<pair<double, int>> currentFrequencies;
    map<int, int> characterFrequencies;
    int totalCharacters = 0;
    for (int i = 0; i < ciphertext.size(); i++)
    {
        if (ciphertext[i] >= 'a' && ciphertext[i] <= 'z')
        {
            totalCharacters++;
            characterFrequencies[ciphertext[i] - 'a']++;
        }
    }
    for (auto character : characterFrequencies)
    {
        double fraction = (character.second / (double)totalCharacters) * 100;
        currentFrequencies.push_back({fraction, character.first});
    }
    sort(currentFrequencies.rbegin(), currentFrequencies.rend());
    string decryptedText = ciphertext;

    string alphabet = "qwertyasdfgzxcvb";
    string substitutionKey = alphabet;
    for (int i = 0; i < alphabet.size(); i++)
    {
        int characterIndex = alphabet[i] - 'a';
        for (int j = 0; j < currentFrequencies.size(); j++)
        {
            auto characterFreq = currentFrequencies[j];
            if (characterFreq.second == characterIndex)
            {
                substitutionKey[i] = (char)(frequencies[j].second + 'a');
                break;
            }
        }
    }
    cout << "Substitution Key: " << substitutionKey << "\n";
    for (int i = 0; i < ciphertext.size(); i++)
    {
        int characterIndex = ciphertext[i] - 'a';
        for (int j = 0; j < currentFrequencies.size(); j++)
        {
            auto characterFreq = currentFrequencies[j];
            if (characterFreq.second == characterIndex)
            {
                decryptedText[i] = (char)(frequencies[j].second + 'a');
                break;
            }
        }
    }
    cout << "Decrypted Text: " << decryptedText << "\n";
    return 0;
}
