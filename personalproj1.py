{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "0658c37c",
   "metadata": {},
   "source": [
    "**Dataset include**\n",
    "1. id: unique id for a news article\n",
    "2. title: the title of a news article\n",
    "3. author: author of the news article\n",
    "4. text: the text of the article; could be incomplete\n",
    "5. label: a label that marks whether the news article is real or fake:\n",
    "         1: Fake news\n",
    "         0: real News\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "a0e3a865",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[31mERROR: Could not find a version that satisfies the requirement TfidfVectorizer (from versions: none)\u001b[0m\r\n",
      "\u001b[31mERROR: No matching distribution found for TfidfVectorizer\u001b[0m\r\n"
     ]
    }
   ],
   "source": [
    "!pip install TfidfVectorizer"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "f0c1504d",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import re\n",
    "from nltk.corpus import stopwords\n",
    "from nltk.stem.porter import PorterStemmer\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.linear_model import LogisticRegression\n",
    "from sklearn.metrics import accuracy_score\n",
    "from sklearn.feature_extraction.text import TfidfVectorizer\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "bddfbe50",
   "metadata": {
    "scrolled": false
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "[nltk_data] Downloading package stopwords to /Users/tarun/nltk_data...\n",
      "[nltk_data]   Unzipping corpora/stopwords.zip.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 21,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import nltk\n",
    "nltk.download('stopwords')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "id": "aa571578",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', \"you're\", \"you've\", \"you'll\", \"you'd\", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', \"she's\", 'her', 'hers', 'herself', 'it', \"it's\", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', \"that'll\", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', \"don't\", 'should', \"should've\", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', \"aren't\", 'couldn', \"couldn't\", 'didn', \"didn't\", 'doesn', \"doesn't\", 'hadn', \"hadn't\", 'hasn', \"hasn't\", 'haven', \"haven't\", 'isn', \"isn't\", 'ma', 'mightn', \"mightn't\", 'mustn', \"mustn't\", 'needn', \"needn't\", 'shan', \"shan't\", 'shouldn', \"shouldn't\", 'wasn', \"wasn't\", 'weren', \"weren't\", 'won', \"won't\", 'wouldn', \"wouldn't\"]\n"
     ]
    }
   ],
   "source": [
    "# printing the stopwords in English\n",
    "print(stopwords.words('english'))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "54b27902",
   "metadata": {},
   "source": [
    "Data Processing"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "id": "f457cc4a",
   "metadata": {},
   "outputs": [],
   "source": [
    "# loading the dataset to a pandas DataFrame\n",
    "news_data=pd.read_csv('/Users/tarun/Downloads/fake-news/train.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "id": "b3fe38a4",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(20800, 5)"
      ]
     },
     "execution_count": 35,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "news_data.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "id": "1ffeb2c9",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>id</th>\n",
       "      <th>title</th>\n",
       "      <th>author</th>\n",
       "      <th>text</th>\n",
       "      <th>label</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>House Dem Aide: We Didn’t Even See Comey’s Let...</td>\n",
       "      <td>Darrell Lucus</td>\n",
       "      <td>House Dem Aide: We Didn’t Even See Comey’s Let...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1</td>\n",
       "      <td>FLYNN: Hillary Clinton, Big Woman on Campus - ...</td>\n",
       "      <td>Daniel J. Flynn</td>\n",
       "      <td>Ever get the feeling your life circles the rou...</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>2</td>\n",
       "      <td>Why the Truth Might Get You Fired</td>\n",
       "      <td>Consortiumnews.com</td>\n",
       "      <td>Why the Truth Might Get You Fired October 29, ...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>3</td>\n",
       "      <td>15 Civilians Killed In Single US Airstrike Hav...</td>\n",
       "      <td>Jessica Purkiss</td>\n",
       "      <td>Videos 15 Civilians Killed In Single US Airstr...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>4</td>\n",
       "      <td>Iranian woman jailed for fictional unpublished...</td>\n",
       "      <td>Howard Portnoy</td>\n",
       "      <td>Print \\nAn Iranian woman has been sentenced to...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   id                                              title              author  \\\n",
       "0   0  House Dem Aide: We Didn’t Even See Comey’s Let...       Darrell Lucus   \n",
       "1   1  FLYNN: Hillary Clinton, Big Woman on Campus - ...     Daniel J. Flynn   \n",
       "2   2                  Why the Truth Might Get You Fired  Consortiumnews.com   \n",
       "3   3  15 Civilians Killed In Single US Airstrike Hav...     Jessica Purkiss   \n",
       "4   4  Iranian woman jailed for fictional unpublished...      Howard Portnoy   \n",
       "\n",
       "                                                text  label  \n",
       "0  House Dem Aide: We Didn’t Even See Comey’s Let...      1  \n",
       "1  Ever get the feeling your life circles the rou...      0  \n",
       "2  Why the Truth Might Get You Fired October 29, ...      1  \n",
       "3  Videos 15 Civilians Killed In Single US Airstr...      1  \n",
       "4  Print \\nAn Iranian woman has been sentenced to...      1  "
      ]
     },
     "execution_count": 36,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "news_data.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "id": "a7634223",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "id           0\n",
       "title      558\n",
       "author    1957\n",
       "text        39\n",
       "label        0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 39,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#Counting the nimber of missing values in the dataset\n",
    "news_data.isnull().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "id": "107fa179",
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "# Replacing the missing values with the null string\n",
    "news_data=news_data.fillna('')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "id": "d6916555",
   "metadata": {},
   "outputs": [],
   "source": [
    "#merging the author name and title column\n",
    "news_data['content']=news_data['author']+' ' +news_data['title']\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "id": "e79783f5",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0        Darrell Lucus House Dem Aide: We Didn’t Even S...\n",
      "1        Daniel J. Flynn FLYNN: Hillary Clinton, Big Wo...\n",
      "2        Consortiumnews.com Why the Truth Might Get You...\n",
      "3        Jessica Purkiss 15 Civilians Killed In Single ...\n",
      "4        Howard Portnoy Iranian woman jailed for fictio...\n",
      "                               ...                        \n",
      "20795    Jerome Hudson Rapper T.I.: Trump a ’Poster Chi...\n",
      "20796    Benjamin Hoffman N.F.L. Playoffs: Schedule, Ma...\n",
      "20797    Michael J. de la Merced and Rachel Abrams Macy...\n",
      "20798    Alex Ansary NATO, Russia To Hold Parallel Exer...\n",
      "20799              David Swanson What Keeps the F-35 Alive\n",
      "Name: content, Length: 20800, dtype: object\n"
     ]
    }
   ],
   "source": [
    "print(news_data['content'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 53,
   "id": "5f0ee004",
   "metadata": {},
   "outputs": [],
   "source": [
    "#separating the data and label\n",
    "X=news_data.drop(columns='label',axis='1')\n",
    "Y=news_data['label']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 55,
   "id": "4ca35611",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "          id                                              title  \\\n",
      "0          0  House Dem Aide: We Didn’t Even See Comey’s Let...   \n",
      "1          1  FLYNN: Hillary Clinton, Big Woman on Campus - ...   \n",
      "2          2                  Why the Truth Might Get You Fired   \n",
      "3          3  15 Civilians Killed In Single US Airstrike Hav...   \n",
      "4          4  Iranian woman jailed for fictional unpublished...   \n",
      "...      ...                                                ...   \n",
      "20795  20795  Rapper T.I.: Trump a ’Poster Child For White S...   \n",
      "20796  20796  N.F.L. Playoffs: Schedule, Matchups and Odds -...   \n",
      "20797  20797  Macy’s Is Said to Receive Takeover Approach by...   \n",
      "20798  20798  NATO, Russia To Hold Parallel Exercises In Bal...   \n",
      "20799  20799                          What Keeps the F-35 Alive   \n",
      "\n",
      "                                          author  \\\n",
      "0                                  Darrell Lucus   \n",
      "1                                Daniel J. Flynn   \n",
      "2                             Consortiumnews.com   \n",
      "3                                Jessica Purkiss   \n",
      "4                                 Howard Portnoy   \n",
      "...                                          ...   \n",
      "20795                              Jerome Hudson   \n",
      "20796                           Benjamin Hoffman   \n",
      "20797  Michael J. de la Merced and Rachel Abrams   \n",
      "20798                                Alex Ansary   \n",
      "20799                              David Swanson   \n",
      "\n",
      "                                                    text  \\\n",
      "0      House Dem Aide: We Didn’t Even See Comey’s Let...   \n",
      "1      Ever get the feeling your life circles the rou...   \n",
      "2      Why the Truth Might Get You Fired October 29, ...   \n",
      "3      Videos 15 Civilians Killed In Single US Airstr...   \n",
      "4      Print \\nAn Iranian woman has been sentenced to...   \n",
      "...                                                  ...   \n",
      "20795  Rapper T. I. unloaded on black celebrities who...   \n",
      "20796  When the Green Bay Packers lost to the Washing...   \n",
      "20797  The Macy’s of today grew from the union of sev...   \n",
      "20798  NATO, Russia To Hold Parallel Exercises In Bal...   \n",
      "20799    David Swanson is an author, activist, journa...   \n",
      "\n",
      "                                                 content  \n",
      "0      Darrell Lucus House Dem Aide: We Didn’t Even S...  \n",
      "1      Daniel J. Flynn FLYNN: Hillary Clinton, Big Wo...  \n",
      "2      Consortiumnews.com Why the Truth Might Get You...  \n",
      "3      Jessica Purkiss 15 Civilians Killed In Single ...  \n",
      "4      Howard Portnoy Iranian woman jailed for fictio...  \n",
      "...                                                  ...  \n",
      "20795  Jerome Hudson Rapper T.I.: Trump a ’Poster Chi...  \n",
      "20796  Benjamin Hoffman N.F.L. Playoffs: Schedule, Ma...  \n",
      "20797  Michael J. de la Merced and Rachel Abrams Macy...  \n",
      "20798  Alex Ansary NATO, Russia To Hold Parallel Exer...  \n",
      "20799            David Swanson What Keeps the F-35 Alive  \n",
      "\n",
      "[20800 rows x 5 columns]\n",
      "0        1\n",
      "1        0\n",
      "2        1\n",
      "3        1\n",
      "4        1\n",
      "        ..\n",
      "20795    0\n",
      "20796    0\n",
      "20797    0\n",
      "20798    1\n",
      "20799    1\n",
      "Name: label, Length: 20800, dtype: int64\n"
     ]
    }
   ],
   "source": [
    "print(X)\n",
    "print(Y)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ab649be2",
   "metadata": {},
   "source": [
    "Stemming, it is a process a reducing a word to its root word and is used to determine domain vocabularies in domain analysis.\n",
    "eg. likes,liking,likely,liked-->lik"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "id": "567b2777",
   "metadata": {},
   "outputs": [],
   "source": [
    "porter_stem=PorterStemmer()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 68,
   "id": "4b8652ad",
   "metadata": {},
   "outputs": [],
   "source": [
    "def stemming(content):\n",
    "    stemmed_content = re.sub('[^a-zA-Z]',' ',content)\n",
    "    stemmed_content = stemmed_content.lower()\n",
    "    stemmed_content = stemmed_content.split()\n",
    "    stemmed_content = [porter_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]\n",
    "    stemmed_content = ' '.join(stemmed_content)\n",
    "    return stemmed_content"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 71,
   "id": "47702a4e",
   "metadata": {},
   "outputs": [],
   "source": [
    "news_data['content']=news_data['content'].apply(stemming)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 72,
   "id": "59973498",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0        darrel lucu hous dem aid even see comey letter...\n",
      "1        daniel j flynn flynn hillari clinton big woman...\n",
      "2                   consortiumnew com truth might get fire\n",
      "3        jessica purkiss civilian kill singl us airstri...\n",
      "4        howard portnoy iranian woman jail fiction unpu...\n",
      "                               ...                        \n",
      "20795    jerom hudson rapper trump poster child white s...\n",
      "20796    benjamin hoffman n f l playoff schedul matchup...\n",
      "20797    michael j de la merc rachel abram maci said re...\n",
      "20798    alex ansari nato russia hold parallel exercis ...\n",
      "20799                            david swanson keep f aliv\n",
      "Name: content, Length: 20800, dtype: object\n"
     ]
    }
   ],
   "source": [
    "print(news_data['content'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 73,
   "id": "a8efcb9f",
   "metadata": {},
   "outputs": [],
   "source": [
    "#separating data and label\n",
    "X=news_data['content'].values\n",
    "Y=news_data['label'].values\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 74,
   "id": "323fd036",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['darrel lucu hous dem aid even see comey letter jason chaffetz tweet'\n",
      " 'daniel j flynn flynn hillari clinton big woman campu breitbart'\n",
      " 'consortiumnew com truth might get fire' ...\n",
      " 'michael j de la merc rachel abram maci said receiv takeov approach hudson bay new york time'\n",
      " 'alex ansari nato russia hold parallel exercis balkan'\n",
      " 'david swanson keep f aliv']\n"
     ]
    }
   ],
   "source": [
    "print(X)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 75,
   "id": "8680c087",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[1 0 1 ... 0 1 1]\n"
     ]
    }
   ],
   "source": [
    "print(Y)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 77,
   "id": "9d00ff5b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(20800,)"
      ]
     },
     "execution_count": 77,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "Y.shape\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 78,
   "id": "ec21a25c",
   "metadata": {},
   "outputs": [],
   "source": [
    "# converting the textual data to numerical data\n",
    "vectorizer = TfidfVectorizer()\n",
    "vectorizer.fit(X)\n",
    "\n",
    "X = vectorizer.transform(X)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 79,
   "id": "a4310d61",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "  (0, 15686)\t0.28485063562728646\n",
      "  (0, 13473)\t0.2565896679337957\n",
      "  (0, 8909)\t0.3635963806326075\n",
      "  (0, 8630)\t0.29212514087043684\n",
      "  (0, 7692)\t0.24785219520671603\n",
      "  (0, 7005)\t0.21874169089359144\n",
      "  (0, 4973)\t0.233316966909351\n",
      "  (0, 3792)\t0.2705332480845492\n",
      "  (0, 3600)\t0.3598939188262559\n",
      "  (0, 2959)\t0.2468450128533713\n",
      "  (0, 2483)\t0.3676519686797209\n",
      "  (0, 267)\t0.27010124977708766\n",
      "  (1, 16799)\t0.30071745655510157\n",
      "  (1, 6816)\t0.1904660198296849\n",
      "  (1, 5503)\t0.7143299355715573\n",
      "  (1, 3568)\t0.26373768806048464\n",
      "  (1, 2813)\t0.19094574062359204\n",
      "  (1, 2223)\t0.3827320386859759\n",
      "  (1, 1894)\t0.15521974226349364\n",
      "  (1, 1497)\t0.2939891562094648\n",
      "  (2, 15611)\t0.41544962664721613\n",
      "  (2, 9620)\t0.49351492943649944\n",
      "  (2, 5968)\t0.3474613386728292\n",
      "  (2, 5389)\t0.3866530551182615\n",
      "  (2, 3103)\t0.46097489583229645\n",
      "  :\t:\n",
      "  (20797, 13122)\t0.2482526352197606\n",
      "  (20797, 12344)\t0.27263457663336677\n",
      "  (20797, 12138)\t0.24778257724396507\n",
      "  (20797, 10306)\t0.08038079000566466\n",
      "  (20797, 9588)\t0.174553480255222\n",
      "  (20797, 9518)\t0.2954204003420313\n",
      "  (20797, 8988)\t0.36160868928090795\n",
      "  (20797, 8364)\t0.22322585870464118\n",
      "  (20797, 7042)\t0.21799048897828688\n",
      "  (20797, 3643)\t0.21155500613623743\n",
      "  (20797, 1287)\t0.33538056804139865\n",
      "  (20797, 699)\t0.30685846079762347\n",
      "  (20797, 43)\t0.29710241860700626\n",
      "  (20798, 13046)\t0.22363267488270608\n",
      "  (20798, 11052)\t0.4460515589182236\n",
      "  (20798, 10177)\t0.3192496370187028\n",
      "  (20798, 6889)\t0.32496285694299426\n",
      "  (20798, 5032)\t0.4083701450239529\n",
      "  (20798, 1125)\t0.4460515589182236\n",
      "  (20798, 588)\t0.3112141524638974\n",
      "  (20798, 350)\t0.28446937819072576\n",
      "  (20799, 14852)\t0.5677577267055112\n",
      "  (20799, 8036)\t0.45983893273780013\n",
      "  (20799, 3623)\t0.37927626273066584\n",
      "  (20799, 377)\t0.5677577267055112\n"
     ]
    }
   ],
   "source": [
    "print(X)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "0d0fd604",
   "metadata": {},
   "source": [
    "Splitting the dataset to training & test data\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 80,
   "id": "4e46b9f7",
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, stratify=Y, random_state=2)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d542b616",
   "metadata": {},
   "source": [
    "Training the Model: Logistic Regression\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 81,
   "id": "8429e739",
   "metadata": {},
   "outputs": [],
   "source": [
    "model = LogisticRegression()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 82,
   "id": "47bfc197",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "LogisticRegression()"
      ]
     },
     "execution_count": 82,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model.fit(X_train, Y_train)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "bf225751",
   "metadata": {},
   "source": [
    "**Evaluation**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 85,
   "id": "3f2e133d",
   "metadata": {},
   "outputs": [],
   "source": [
    "# accuracy score on the training data\n",
    "X_train_prediction = model.predict(X_train)\n",
    "training_data_accuracy = accuracy_score(X_train_prediction, Y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 86,
   "id": "c871304d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy score of the training data :  0.9865985576923076\n"
     ]
    }
   ],
   "source": [
    "print('Accuracy score of the training data : ', training_data_accuracy)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 89,
   "id": "98994453",
   "metadata": {},
   "outputs": [],
   "source": [
    "# accuracy score on the test data\n",
    "X_test_prediction = model.predict(X_test)\n",
    "test_data_accuracy = accuracy_score(X_test_prediction, Y_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 90,
   "id": "3aff78f0",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy score of the test data :  0.9790865384615385\n"
     ]
    }
   ],
   "source": [
    "print('Accuracy score of the test data : ', test_data_accuracy)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 91,
   "id": "748c664d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[0]\n",
      "The news is Real\n"
     ]
    }
   ],
   "source": [
    "X_new = X_test[3]\n",
    "\n",
    "prediction = model.predict(X_new)\n",
    "print(prediction)\n",
    "\n",
    "if (prediction[0]==0):\n",
    "  print('The news is Real')\n",
    "else:\n",
    "  print('The news is Fake')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 92,
   "id": "f1270629",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0\n"
     ]
    }
   ],
   "source": [
    "print(Y_test[3])"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
