import { useState, useEffect } from 'react';
import { NextPage } from 'next';
import Head from 'next/head';
import { useRouter } from 'next/router';

interface Idea {
  id: string;
  text: string;
  normalized: string;
  count: number;
  country: string;
  city: string;
  createdAt: string;
}

const IdeasPage: NextPage = () => {
  const router = useRouter();
  const { country, city } = router.query;

  const [ideaText, setIdeaText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showIdeas, setShowIdeas] = useState(false);
  const [ideas, setIdeas] = useState<Idea[]>([]);

  useEffect(() => {
    if (showIdeas && country && city) {
      fetchIdeas();
    }
  }, [showIdeas, country, city]);

  const fetchIdeas = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/ideas?country=${country}&city=${city}`);
      if (response.ok) {
        const data = await response.json();
        setIdeas(data);
      }
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ideaText.trim()) return;

    setIsSubmitting(true);
    try {
      const response = await fetch('http://localhost:8000/api/ideas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: ideaText,
          country,
          city,
        }),
      });

      if (response.ok) {
        setIdeaText('');
        alert('✅ Votre idée a été enregistrée !');
      }
    } catch (error) {
      alert('❌ Erreur lors de l\'enregistrement');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!country || !city) {
    return <div className="min-h-screen flex items-center justify-center">Chargement...</div>;
  }

  return (
    <>
      <Head>
        <title>Partagez vos idées - {city}, {country}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Header */}
        <div className="bg-white shadow-sm">
          <div className="max-w-4xl mx-auto px-4 py-3 sm:py-4 flex items-center justify-between">
            <button
              onClick={() => router.push('/')}
              className="text-blue-600 hover:text-blue-700 flex items-center gap-1 sm:gap-2 text-sm sm:text-base"
            >
              ← <span className="hidden xs:inline">Changer de </span>lieu
            </button>
            <div className="flex items-center gap-2">
              <span className="text-xl sm:text-2xl font-bold text-blue-600">BALANCE</span>
            </div>
          </div>
        </div>

        <div className="max-w-4xl mx-auto px-4 py-6 sm:py-8">
          {/* Location badge */}
          <div className="text-center mb-6 sm:mb-8">
            <div className="inline-flex items-center gap-2 bg-white px-4 sm:px-6 py-2 sm:py-3 rounded-full shadow-md">
              <span className="text-xl sm:text-2xl">📍</span>
              <span className="font-semibold text-gray-900 text-sm sm:text-base">{city}</span>
              <span className="text-gray-400">•</span>
              <span className="text-gray-600 text-sm sm:text-base">{country}</span>
            </div>
          </div>

          {!showIdeas ? (
            /* Submit form */
            <div className="bg-white rounded-xl sm:rounded-2xl shadow-xl p-6 sm:p-8 space-y-4 sm:space-y-6">
              <div className="text-center">
                <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-3">
                  Quelle est votre idée ?
                </h1>
                <p className="text-sm sm:text-base text-gray-600">
                  Exprimez vos revendications, envies ou idées pour améliorer votre ville
                </p>
              </div>

              {/* Examples */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-sm font-medium text-blue-900 mb-2">💡 Exemples :</p>
                <ul className="text-sm text-blue-800 space-y-1">
                  <li>• "Une piscine municipale gratuite"</li>
                  <li>• "Plus de pistes cyclables sécurisées"</li>
                  <li>• "Réduire la pollution de l'air"</li>
                  <li>• "Créer un espace vert dans le quartier"</li>
                </ul>
              </div>

              {/* Form */}
              <form onSubmit={handleSubmit} className="space-y-4">
                <textarea
                  value={ideaText}
                  onChange={(e) => setIdeaText(e.target.value)}
                  placeholder="Écrivez votre idée ici..."
                  rows={6}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition resize-none text-base sm:text-lg"
                  maxLength={500}
                />
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-0">
                  <span className="text-xs sm:text-sm text-gray-500">
                    {ideaText.length}/500 caractères
                  </span>
                  <button
                    type="submit"
                    disabled={isSubmitting || !ideaText.trim()}
                    className="w-full sm:w-auto bg-blue-600 text-white px-6 sm:px-8 py-3 rounded-lg hover:bg-blue-700 transition font-medium disabled:bg-gray-300 disabled:cursor-not-allowed text-sm sm:text-base"
                  >
                    {isSubmitting ? 'Envoi...' : 'Partager mon idée'}
                  </button>
                </div>
              </form>

              {/* View ideas button */}
              <div className="pt-6 border-t border-gray-200">
                <button
                  onClick={() => setShowIdeas(true)}
                  className="w-full bg-gray-100 text-gray-700 py-4 px-6 rounded-lg hover:bg-gray-200 transition font-medium"
                >
                  📊 Voir les idées déjà proposées
                </button>
              </div>
            </div>
          ) : (
            /* Ideas list */
            <div className="bg-white rounded-xl sm:rounded-2xl shadow-xl p-6 sm:p-8 space-y-4 sm:space-y-6">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-0">
                <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">
                  Idées proposées
                </h1>
                <button
                  onClick={() => setShowIdeas(false)}
                  className="text-blue-600 hover:text-blue-700 font-medium text-sm sm:text-base"
                >
                  ← Proposer une idée
                </button>
              </div>

              <p className="text-sm sm:text-base text-gray-600">
                Les idées similaires sont regroupées automatiquement par l'IA
              </p>

              {/* Stats */}
              <div className="grid grid-cols-2 gap-3 sm:gap-4">
                <div className="bg-blue-50 p-3 sm:p-4 rounded-lg">
                  <div className="text-xl sm:text-2xl font-bold text-blue-600">{ideas.length}</div>
                  <div className="text-xs sm:text-sm text-gray-600">Idées uniques</div>
                </div>
                <div className="bg-green-50 p-3 sm:p-4 rounded-lg">
                  <div className="text-xl sm:text-2xl font-bold text-green-600">
                    {ideas.reduce((sum, idea) => sum + idea.count, 0)}
                  </div>
                  <div className="text-xs sm:text-sm text-gray-600">Contributions totales</div>
                </div>
              </div>

              {/* Ideas list */}
              <div className="space-y-4">
                {ideas.length === 0 ? (
                  <div className="text-center py-12 text-gray-500">
                    Aucune idée pour le moment. Soyez le premier !
                  </div>
                ) : (
                  ideas
                    .sort((a, b) => b.count - a.count)
                    .map((idea) => (
                      <div
                        key={idea.id}
                        className="border-2 border-gray-200 rounded-lg p-4 sm:p-6 hover:border-blue-300 transition"
                      >
                        <div className="flex items-start justify-between gap-3 sm:gap-4">
                          <div className="flex-1 min-w-0">
                            <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2 break-words">
                              {idea.normalized}
                            </h3>
                            <p className="text-xs sm:text-sm text-gray-600 italic break-words">
                              Ex: "{idea.text}"
                            </p>
                          </div>
                          <div className="flex flex-col items-center gap-1 flex-shrink-0">
                            <div className="bg-blue-100 text-blue-700 font-bold text-lg sm:text-xl px-3 sm:px-4 py-1 sm:py-2 rounded-lg">
                              {idea.count}
                            </div>
                            <span className="text-xs text-gray-500 whitespace-nowrap">
                              {idea.count === 1 ? 'personne' : 'personnes'}
                            </span>
                          </div>
                        </div>

                        {/* Progress bar */}
                        <div className="mt-4">
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full transition-all"
                              style={{
                                width: `${Math.min(
                                  (idea.count / Math.max(...ideas.map((i) => i.count))) * 100,
                                  100
                                )}%`,
                              }}
                            />
                          </div>
                        </div>
                      </div>
                    ))
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default IdeasPage;
