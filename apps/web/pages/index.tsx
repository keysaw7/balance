import { useState } from 'react';
import { NextPage } from 'next';
import Head from 'next/head';
import { useRouter } from 'next/router';

const Home: NextPage = () => {
  const router = useRouter();
  const [step, setStep] = useState<'country' | 'city'>('country');
  const [country, setCountry] = useState('');
  const [city, setCity] = useState('');
  const [customCountry, setCustomCountry] = useState('');
  const [customCity, setCustomCity] = useState('');
  const [useLocation, setUseLocation] = useState(false);
  const [isValidating, setIsValidating] = useState(false);

  const suggestedCountries = ['France', 'Belgique', 'Suisse', 'Canada', 'Luxembourg', 'États-Unis', 'Royaume-Uni', 'Allemagne', 'Espagne', 'Italie'];

  const handleLocationRequest = () => {
    setUseLocation(true);
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          // Simulation - en prod, utiliser une API de géolocalisation inverse
          setCountry('France');
          setCity('Paris');
          setStep('city');
        },
        (error) => {
          alert('Impossible d\'accéder à votre localisation');
          setUseLocation(false);
        }
      );
    }
  };

  const handleCountrySelect = (selectedCountry: string) => {
    setCountry(selectedCountry);
    setCustomCountry('');
    setStep('city');
  };

  const handleCustomCountrySubmit = () => {
    if (customCountry.trim()) {
      setCountry(customCountry.trim());
      setStep('city');
    }
  };

  const validateCity = async (cityName: string, countryName: string) => {
    if (!cityName.trim()) return false;
    
    setIsValidating(true);
    try {
      // Appel à l'API Nominatim via notre backend
      const response = await fetch(
        `http://localhost:8000/api/geocoding/validate?city=${encodeURIComponent(cityName)}&country=${encodeURIComponent(countryName)}`
      );
      
      if (response.ok) {
        const data = await response.json();
        
        if (data.valid) {
          // Utiliser le nom normalisé pour éviter les doublons
          if (data.normalized_name) {
            setCustomCity(data.normalized_name);
          }
          
          if (data.fallback) {
            console.log('Validation en mode dégradé (timeout ou erreur API)');
          } else {
            console.log(`Ville validée: ${data.display_name}`);
            console.log(`  - Nom normalisé: ${data.normalized_name}`);
            console.log(`  - OSM ID: ${data.osm_id}`);
            console.log(`  - Code postal: ${data.postal_code || 'N/A'}`);
          }
          return true;
        } else {
          return false;
        }
      } else {
        // En cas d'erreur API, on accepte quand même (mode dégradé)
        console.warn('API validation failed, fallback mode');
        // Normaliser manuellement
        setCustomCity(cityName.trim().charAt(0).toUpperCase() + cityName.trim().slice(1).toLowerCase());
        return cityName.trim().length > 2;
      }
    } catch (error) {
      console.error('Validation error:', error);
      // En cas d'erreur, normaliser manuellement
      setCustomCity(cityName.trim().charAt(0).toUpperCase() + cityName.trim().slice(1).toLowerCase());
      return cityName.trim().length > 2;
    } finally {
      setIsValidating(false);
    }
  };

  const handleValidate = async () => {
    const finalCity = customCity.trim() || city;
    const finalCountry = country;
    
    if (finalCountry && finalCity) {
      const isValid = await validateCity(finalCity, finalCountry);
      if (isValid) {
        router.push(`/ideas?country=${encodeURIComponent(finalCountry)}&city=${encodeURIComponent(finalCity)}`);
      } else {
        alert(`❌ "${finalCity}" n'a pas été trouvée dans ${finalCountry}.\n\nVérifiez l'orthographe ou essayez une ville proche.`);
      }
    }
  };

  return (
    <>
      <Head>
        <title>BALANCE - Partagez vos idées citoyennes</title>
        <meta name="description" content="Partagez vos idées et revendications pour votre ville, votre pays" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4 sm:p-6 md:p-8">
        <div className="max-w-2xl w-full">
          {/* Logo */}
          <div className="text-center mb-6 sm:mb-8">
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-blue-600 mb-2">BALANCE</h1>
            <p className="text-sm sm:text-base text-gray-600">Votre voix compte</p>
          </div>

          {/* Main Card */}
          <div className="bg-white rounded-xl sm:rounded-2xl shadow-xl p-6 sm:p-8">
            {/* Step Country */}
            {step === 'country' && (
              <div className="space-y-4 sm:space-y-6">
                <div className="text-center">
                  <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-2">
                    Choisissez votre pays
                  </h2>
                  <p className="text-sm sm:text-base text-gray-600">
                    Où souhaitez-vous partager vos idées ?
                  </p>
                </div>

                {/* Location button */}
                <button
                  onClick={handleLocationRequest}
                  className="w-full bg-blue-50 border-2 border-blue-200 text-blue-700 py-3 px-4 rounded-lg hover:bg-blue-100 transition flex items-center justify-center gap-2"
                >
                  <span className="text-xl">📍</span>
                  Utiliser ma localisation
                </button>

                <div className="relative">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-gray-300"></div>
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-4 bg-white text-gray-500">ou choisir manuellement</span>
                  </div>
                </div>

                {/* Countries list */}
                <div className="space-y-3">
                  <p className="text-xs sm:text-sm text-gray-600 font-medium">Suggestions :</p>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3">
                    {suggestedCountries.map((c) => (
                      <button
                        key={c}
                        onClick={() => handleCountrySelect(c)}
                        className="text-left py-3 px-3 sm:px-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition"
                      >
                        <span className="text-sm font-medium text-gray-900">{c}</span>
                      </button>
                    ))}
                  </div>

                  <div className="relative">
                    <div className="absolute inset-0 flex items-center">
                      <div className="w-full border-t border-gray-300"></div>
                    </div>
                    <div className="relative flex justify-center text-sm">
                      <span className="px-4 bg-white text-gray-500">ou</span>
                    </div>
                  </div>

                  {/* Custom country input */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Saisissez votre pays :
                    </label>
                    <div className="flex gap-2">
                      <input
                        type="text"
                        value={customCountry}
                        onChange={(e) => setCustomCountry(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleCustomCountrySubmit()}
                        placeholder="Ex: Maroc, Tunisie, Sénégal..."
                        className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none"
                      />
                      <button
                        onClick={handleCustomCountrySubmit}
                        disabled={!customCountry.trim()}
                        className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition font-medium disabled:bg-gray-300 disabled:cursor-not-allowed"
                      >
                        →
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Step City */}
            {step === 'city' && country && (
              <div className="space-y-4 sm:space-y-6">
                <button
                  onClick={() => {
                    setStep('country');
                    setCity('');
                    setCustomCity('');
                  }}
                  className="text-blue-600 hover:text-blue-700 flex items-center gap-2 text-sm sm:text-base"
                >
                  ← Retour
                </button>

                <div className="text-center">
                  <div className="inline-block bg-blue-100 text-blue-700 px-3 sm:px-4 py-1 rounded-full text-xs sm:text-sm mb-4">
                    {country}
                  </div>
                  <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-2">
                    Quelle est votre ville ?
                  </h2>
                  <p className="text-sm sm:text-base text-gray-600">
                    Entrez le nom de votre ville
                  </p>
                </div>

                {/* Custom city input */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Nom de la ville :
                  </label>
                  <input
                    type="text"
                    value={customCity}
                    onChange={(e) => setCustomCity(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleValidate()}
                    placeholder="Ex: Casablanca, Tunis, Dakar, Montréal..."
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none text-lg"
                    autoFocus
                  />
                  <p className="mt-2 text-sm text-gray-500">
                    💡 Entrez n'importe quelle ville dans le monde
                  </p>
                </div>

                {/* Validate button */}
                <button
                  onClick={handleValidate}
                  disabled={!customCity.trim() || isValidating}
                  className="w-full bg-blue-600 text-white py-4 px-6 rounded-lg hover:bg-blue-700 transition font-medium text-lg disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  {isValidating ? 'Validation...' : 'Continuer →'}
                </button>
              </div>
            )}
          </div>

          {/* Footer */}
          <p className="text-center text-gray-600 text-xs sm:text-sm mt-6 px-4">
            Projet open source • Anonyme • Transparent
          </p>
        </div>
      </div>
    </>
  );
};

export default Home;
