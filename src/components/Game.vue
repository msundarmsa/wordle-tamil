<template>
    <div id="game">
        <header>
            <div class="header-left">
                <div class="help icon" @click="helpOpened = true">
                    <svg xmlns="http://www.w3.org/2000/svg" class="ionicon" viewBox="0 0 512 512"><title>Aide</title><path d="M256 80a176 176 0 10176 176A176 176 0 00256 80z" fill="none" stroke="currentColor" stroke-miterlimit="10" stroke-width="32"/><path d="M200 202.29s.84-17.5 19.57-32.57C230.68 160.77 244 158.18 256 158c10.93-.14 20.69 1.67 26.53 4.45 10 4.76 29.47 16.38 29.47 41.09 0 26-17 37.81-36.37 50.8S251 281.43 251 296" fill="none" stroke="currentColor" stroke-linecap="round" stroke-miterlimit="10" stroke-width="28"/><circle cx="250" cy="348" r="20"/></svg>
                </div>
            </div>
            <h1>சொல்லி</h1> <!--MORDLE-->
            <div class="header-right">
                <div class="icon" @click="statsOpened = true">
                    <svg xmlns="http://www.w3.org/2000/svg" class="ionicon" viewBox="0 0 512 512"><title>Statistiques</title><path d="M104 496H72a24 24 0 01-24-24V328a24 24 0 0124-24h32a24 24 0 0124 24v144a24 24 0 01-24 24zM328 496h-32a24 24 0 01-24-24V232a24 24 0 0124-24h32a24 24 0 0124 24v240a24 24 0 01-24 24zM440 496h-32a24 24 0 01-24-24V120a24 24 0 0124-24h32a24 24 0 0124 24v352a24 24 0 01-24 24zM216 496h-32a24 24 0 01-24-24V40a24 24 0 0124-24h32a24 24 0 0124 24v432a24 24 0 01-24 24z"/></svg>
                </div>
                <div class="icon" @click="settingsOpened = true">
                    <svg xmlns="http://www.w3.org/2000/svg" class="ionicon" viewBox="0 0 512 512"><title>Paramètres</title><circle cx="256" cy="256" r="48"/><path d="M470.39 300l-.47-.38-31.56-24.75a16.11 16.11 0 01-6.1-13.33v-11.56a16 16 0 016.11-13.22L469.92 212l.47-.38a26.68 26.68 0 005.9-34.06l-42.71-73.9a1.59 1.59 0 01-.13-.22A26.86 26.86 0 00401 92.14l-.35.13-37.1 14.93a15.94 15.94 0 01-14.47-1.29q-4.92-3.1-10-5.86a15.94 15.94 0 01-8.19-11.82l-5.59-39.59-.12-.72A27.22 27.22 0 00298.76 26h-85.52a26.92 26.92 0 00-26.45 22.39l-.09.56-5.57 39.67a16 16 0 01-8.13 11.82 175.21 175.21 0 00-10 5.82 15.92 15.92 0 01-14.43 1.27l-37.13-15-.35-.14a26.87 26.87 0 00-32.48 11.34l-.13.22-42.77 73.95a26.71 26.71 0 005.9 34.1l.47.38 31.56 24.75a16.11 16.11 0 016.1 13.33v11.56a16 16 0 01-6.11 13.22L42.08 300l-.47.38a26.68 26.68 0 00-5.9 34.06l42.71 73.9a1.59 1.59 0 01.13.22 26.86 26.86 0 0032.45 11.3l.35-.13 37.07-14.93a15.94 15.94 0 0114.47 1.29q4.92 3.11 10 5.86a15.94 15.94 0 018.19 11.82l5.56 39.59.12.72A27.22 27.22 0 00213.24 486h85.52a26.92 26.92 0 0026.45-22.39l.09-.56 5.57-39.67a16 16 0 018.18-11.82c3.42-1.84 6.76-3.79 10-5.82a15.92 15.92 0 0114.43-1.27l37.13 14.95.35.14a26.85 26.85 0 0032.48-11.34 2.53 2.53 0 01.13-.22l42.71-73.89a26.7 26.7 0 00-5.89-34.11zm-134.48-40.24a80 80 0 11-83.66-83.67 80.21 80.21 0 0183.66 83.67z"/></svg>
                </div>
            </div>
        </header>
        <main>
            <transition name="fade">
                <div class="error" v-if="error">{{ error }}</div>
            </transition>
            <div class="grid">
                <div class="attempt" v-for="attempt, indexA in attempts" :key="indexA" :class="{ shake: error && indexA === currentAttempt - 1 }">
                    <LetterContainer 
                        :letter="attempts[indexA][indexL]" 
                        :color="results[indexA][indexL]" 
                        :placement="letter" 
                        :animate="animateLetter" 
                        :colorBlindMode="colorBlindMode"
                        v-for="letter, indexL in NB_LETTERS" 
                        :key="letter" />
                </div>
            </div>
            <div class="keyboard">
                <div class="keyboard-line" v-for="line, index in keyboard.content" :key="index">
                    <Key
                        :keyContent="key"
                        :color="getKeyColor(key)"
                        :colorBlindMode="colorBlindMode"
                        v-for="key in line"
                        :key="key"
                        @update:handleClick="handleKeyClick($event)"
                    />
                </div>
            </div>
            <transition name="fadeup">
                <div class="help-modal" v-if="helpOpened">
                    <div class="help-modal-content">
                        <div class="close-btn" @click="helpOpened = false">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#919191" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
                        </div>
                        <div class="help-content">
                            <h2>எப்படி விளையாடுவது?</h2>
                            <p>தினம் ஒரு ஐந்து எழுத்து சொல் தேர்ந்தெடுக்கப்படும். உங்களுக்கு ஆறு முயற்சிகள் உண்டு</p>
                            <p>ஒவ்வொரு முயற்சியிலும் கீழ்காணும் வரைமுறைக்கு ஏற்றவாறு எழுத்துக்களின் நிறம் மாறும்</p>
                            <div class="help-exemple">
                                <div class="help-word">
                                    <div class="help-letter-container correct" :class="{ 'color-blind': colorBlindMode }">
                                        க
                                    </div>
                                    <div class="help-letter-container">
                                        ச்
                                    </div>
                                    <div class="help-letter-container">
                                        சே
                                    </div>
                                    <div class="help-letter-container">
                                        ரி
                                    </div>
                                </div>
                                <p><span>க</span> என்னும் எழுத்து வார்த்தையில் சரியான இடத்தில் உள்ளது</p>
                                <div class="help-word">
                                    <div class="help-letter-container">
                                        கு
                                    </div>
                                    <div class="help-letter-container">
                                        ழ
                                    </div>
                                    <div class="help-letter-container partial" :class="{ 'color-blind': colorBlindMode }">
                                        ப்
                                    </div>
                                    <div class="help-letter-container">
                                        பு
                                    </div>
                                </div>
                                <p><span>ப்</span> எனும் எழுத்து வார்த்தையில் உள்ளது ஆனால் சரியான இடத்தில் இல்லை</p>
                                <div class="help-word">
                                    <div class="help-letter-container">
                                        பெ
                                    </div>
                                    <div class="help-letter-container partialmei" :class="{ 'color-blind': colorBlindMode }">
                                        ரு
                                    </div>
                                    <div class="help-letter-container">
                                        ம
                                    </div>
                                    <div class="help-letter-container">
                                        ழை
                                    </div>
                                </div>
                                <p><span>ர</span> எனும் எழுத்து உ எனும் உயிரெழுத்தோடு சேராமல் வேறொரு உயிரெழுத்தோடு சேர்ந்து வார்த்தையில் இடம்பெறுகிறது</p>
                                <div class="help-word">
                                    <div class="help-letter-container">
                                        அ
                                    </div>
                                    <div class="help-letter-container">
                                        ன்
                                    </div>
                                    <div class="help-letter-container">
                                        னா
                                    </div>
                                    <div class="help-letter-container incorrect" :class="{ 'color-blind': colorBlindMode }">
                                        சி
                                    </div>
                                </div>
                                <p><span>ச</span> எனும் எழுத்து எந்த ஒரு உயிரெழுத்தோடும் சேர்ந்து வார்த்தையில் இடம்பெறவில்லை</p>
                            </div>
                        </div>
                    </div>
                </div>
            </transition>
            <transition name="fadeup">
                <div class="endgame-modal" v-if="statsOpened">
                    <div class="endgame-modal-content">
                        <div class="close-btn" @click="statsOpened = false">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#919191" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
                        </div>
                        <div class="stats">
                            <h2>புள்ளிவிவரங்கள்</h2>
                            <div class="stats-content">
                                <div class="stats-item games-played">
                                    <p class="stat-item-figure">{{ userResults.nbGames }}</p>
                                    <p class="stat-item-label">முயற்சிகள்</p>
                                </div>
                                <div class="stats-item win-rate">
                                    <p class="stat-item-figure">{{ Math.round((userResults.nbGames > 0 ? userResults.nbWins / userResults.nbGames : 0) * 100) }}</p>
                                    <p class="stat-item-label">வெற்றிகள் (%)</p>
                                </div>
                                <div class="stats-item current-streak">
                                    <p class="stat-item-figure">{{ userResults.currentStreak }}</p>
                                    <p class="stat-item-label">தற்போதைய நேர் வெற்றிகள்</p>
                                </div>
                                <div class="stats-item current-streak">
                                    <p class="stat-item-figure">{{ userResults.bestStreak }}</p>
                                    <p class="stat-item-label">அதிகபட்ச நேர் வேற்றிகள்</p>
                                </div>
                            </div>
                        </div>
                        <div class="graph">
                            <h2>பகிர்மானம்</h2>
                            <div class="graph-content">
                                <div class="graph-item" v-for="attempt in NB_ATTEMPTS + 1" :key="attempt">
                                    <div class="attempt-number" v-if="attempt <= NB_ATTEMPTS">{{ attempt }}</div>
                                    <div class="attempt-skull" v-else>
                                        💀
                                    </div>
                                    <div class="attempt-stat">
                                        <div class="attempt-bar" :class="{ best: getAttemptStatPercent(attempt) === bestAttemptPercent && getAttemptStat(attempt) > 0 }" :style="{ width: `${getAttemptStatPercent(attempt)}%`}">{{ getAttemptStat(attempt) }}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="soluce" v-if="finished">இன்றைய சொல் : 
                            <strong>{{ wordOfTheDay }}</strong> 
                            <a :href="`https://dsal.uchicago.edu/cgi-bin/app/tamil_query.py?qs=${this.wordOfTheDay.toLowerCase()}&searchhws=yes&matchtype=exact`" target="_blank" class="definition-icon">
                                <svg xmlns="http://www.w3.org/2000/svg" class="ionicon" viewBox="0 0 512 512"><title>Définition</title><path d="M256 56C145.72 56 56 145.72 56 256s89.72 200 200 200 200-89.72 200-200S366.28 56 256 56zm0 82a26 26 0 11-26 26 26 26 0 0126-26zm48 226h-88a16 16 0 010-32h28v-88h-16a16 16 0 010-32h32a16 16 0 0116 16v104h28a16 16 0 010 32z"/></svg>
                            </a>
                        </div>
                        <div class="modal-footer" v-if="finished">
                            <div class="next-in">அடுத்த வார்த்தை : <strong class="time">{{ countdownToNextWord }}</strong></div>
                            <div class="separator"></div>
                            <div class="share">
                                <button class="share-button" @click="share">
                                    <p>{{resultsCopied ? 'பிரதி ஆயிற்று!' : 'பகிர்க'}}</p>
                                    <svg v-if="!resultsCopied" xmlns="http://www.w3.org/2000/svg" class="ionicon" viewBox="0 0 512 512"><title>பகிர்க</title><path d="M384 336a63.78 63.78 0 00-46.12 19.7l-148-83.27a63.85 63.85 0 000-32.86l148-83.27a63.8 63.8 0 10-15.73-27.87l-148 83.27a64 64 0 100 88.6l148 83.27A64 64 0 10384 336z"/></svg>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </transition>
            <transition name="fadeup">
                <div class="settings-modal" v-if="settingsOpened">
                    <div class="settings-modal-content">
                        <div class="close-btn" @click="settingsOpened = false">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#919191" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
                        </div>
                        <div class="settings-content">
                            <h2>அமைப்பு</h2>
                            <div class="settings-item setting-toggle">
                                <h3>மாறுபட்ட நிறங்கள்</h3>
                                <div class="toggle-button" @click="colorBlindMode = !colorBlindMode" :class="{ activated: colorBlindMode }">
                                    <div class="toggle"></div>
                                </div>
                            </div>
                            <div class="settings-item setting-toggle">
                                <h3>கடின சொற்கள்</h3>
                                <div class="toggle-button" @click="hardWords = !hardWords" :class="{ activated: hardWords}">
                                    <div class="toggle"></div>
                                </div>
                            </div>
                            <div class="settings-item credits">
                                <h3>நன்றிகள்</h3>
                                <p>
                                    தமிழுக்கு மாற்றி அமைத்தது: <a href="https://msundarmsa.github.io/">msundarmsa</a>.
                                </p>
                                <p>
                                    மென்பொருளுக்கான அடிப்படை: <a href="https://twitter.com/louanben">@louanben</a>.
                                </p>
                                <p>
                                    மூலதன வடிவமைப்பு: <strong>Wordle</strong> by <a href="https://twitter.com/powerlanguish">@powerlanguish</a> (Josh Wardle).
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </transition>
        </main>
    </div>
</template>

<script>
import * as seedrandom from 'seedrandom';
import moment from 'moment-timezone';

import LetterContainer from "./grid/LetterContainer.vue";
import Key from "./keyboard/Key.vue";
import words from "../assets/json/drawable-words.json";
import extwords from "../assets/json/ext-drawable-words.json";
import playableWords from "../assets/json/playable-words.json";

const NB_LETTERS = 4;
const NB_ATTEMPTS = 7;
const ENTER = '⏎';
const BACKSPACE = '⌫';

const KEYBOARD_AZERTY = {
    name: 'azerty',
    content: [
        ['ஆ',  'ஈ',  'ஊ',  'ஏ',  'ள',  'ற',  'ன',  'ட',  'ண',  'ச',  'ஞ'],
        ['அ',  'இ',  'உ',  'ஐ',  'எ',  'க',  'ப',  'ம',  'த',  'ந',  'ய'], 
        [ENTER,  'ஔ',  'ஓ',  'ஒ',  'வ',  'ங',  'ல',  'ர',  'ழ',  '்', BACKSPACE]
    ],
};

const uyir = ['அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ', 'எ', 'ஏ', 'ஐ', 'ஒ', 'ஓ', 'ஔ', '்']
const mei = ['க', 'ங', 'ச', 'ஞ', 'ட', 'ண', 'த', 'ந', 'ப', 'ம', 'ய', 'ர', 'ல', 'வ', 'ழ', 'ள', 'ற', 'ன']
const uyirmei_table = {
    'க': ['க', 'கா', 'கி', 'கீ', 'கு', 'கூ', 'கெ', 'கே', 'கை', 'கொ', 'கோ', 'கௌ', 'க்'],
    'ங': ['ங', 'ஙா', 'ஙி', 'ஙீ', 'ஙு', 'ஙூ', 'ஙெ', 'ஙே', 'ஙை', 'ஙொ', 'ஙோ', 'ஙௌ', 'ங்'],
    'ச': ['ச', 'சா', 'சி', 'சீ', 'சு', 'சூ', 'செ', 'சே', 'சை', 'சொ', 'சோ', 'சௌ', 'ச்'],
    'ஞ': ['ஞ', 'ஞா', 'ஞி', 'ஞீ', 'ஞு', 'ஞூ', 'ஞெ', 'ஞே', 'ஞை', 'ஞொ', 'ஞோ', 'ஞௌ', 'ஞ்'],
    'ட': ['ட', 'டா', 'டி', 'டீ', 'டு', 'டூ', 'டெ', 'டே', 'டை', 'டொ', 'டோ', 'டௌ', 'ட்'],
    'ண': ['ண', 'ணா', 'ணி', 'ணீ', 'ணு', 'ணூ', 'ணெ', 'ணே', 'ணை', 'ணொ', 'ணோ', 'ணௌ', 'ண்'],
    'த': ['த', 'தா', 'தி', 'தீ', 'து', 'தூ', 'தெ', 'தே', 'தை', 'தொ', 'தோ', 'தௌ', 'த்'],
    'ந': ['ந', 'நா', 'நி', 'நீ', 'நு', 'நூ', 'நெ', 'நே', 'நை', 'நொ', 'நோ', 'நௌ', 'ந்'],
    'ப': ['ப', 'பா', 'பி', 'பீ', 'பு', 'பூ', 'பெ', 'பே', 'பை', 'பொ', 'போ', 'பௌ', 'ப்'],
    'ம': ['ம', 'மா', 'மி', 'மீ', 'மு', 'மூ', 'மெ', 'மே', 'மை', 'மொ', 'மோ', 'மௌ', 'ம்'],
    'ய': ['ய', 'யா', 'யி', 'யீ', 'யு', 'யூ', 'யெ', 'யே', 'யை', 'யொ', 'யோ', 'யௌ', 'ய்'],
    'ர': ['ர', 'ரா', 'ரி', 'ரீ', 'ரு', 'ரூ', 'ரெ', 'ரே', 'ரை', 'ரொ', 'ரோ', 'ரௌ', 'ர்'],
    'ல': ['ல', 'லா', 'லி', 'லீ', 'லு', 'லூ', 'லெ', 'லே', 'லை', 'லொ', 'லோ', 'லௌ', 'ல்'],
    'வ': ['வ', 'வா', 'வி', 'வீ', 'வு', 'வூ', 'வெ', 'வே', 'வை', 'வொ', 'வோ', 'வௌ', 'வ்'],
    'ழ': ['ழ', 'ழா', 'ழி', 'ழீ', 'ழு', 'ழூ', 'ழெ', 'ழே', 'ழை', 'ழொ', 'ழோ', 'ழௌ', 'ழ்'],
    'ள': ['ள', 'ளா', 'ளி', 'ளீ', 'ளு', 'ளூ', 'ளெ', 'ளே', 'ளை', 'ளொ', 'ளோ', 'ளௌ', 'ள்'],
    'ற': ['ற', 'றா', 'றி', 'றீ', 'று', 'றூ', 'றெ', 'றே', 'றை', 'றொ', 'றோ', 'றௌ', 'ற்'],
    'ன': ['ன', 'னா', 'னி', 'னீ', 'னு', 'னூ', 'னெ', 'னே', 'னை', 'னொ', 'னோ', 'னௌ', 'ன்']
}

export default {
    name: 'Game',
    components: {
        LetterContainer,
        Key,
    },
    data() {
        return {
            seedrandom,
            NB_LETTERS,
            NB_ATTEMPTS,
            KEYBOARD_AZERTY,
            keyboard: KEYBOARD_AZERTY,
            today: moment(),
            words,
            attempts: [],
            results: [],
            currentAttempt: 1,
            countdownToNextWord: '',
            wordOfTheDay: '',
            error: '',
            correctLetters: [],
            partialLetters: [],
            incorrectLetters: [],
            won: false,
            finished: false,
            statsOpened: false,
            settingsOpened: false,
            helpOpened: false,
            colorBlindMode: false,
            sharedLink: true,
            isStreak: false,
            animateLetter: true,
            bestAttemptPercent: 0,
            resultsCopied: false,
            userResults: {
                nbGames: 0,
                nbWins: 0,
                currentStreak: 0,
                bestStreak: 0,
                games: [],
            },
            uyir,
            mei,
            uyirmei_table,
            ENTER,
            BACKSPACE,
            baseWordOfTheDay: [],
            hardWords: false,
            extwords
            // {
            //     nbGames: 0,
            //     nbWins: 0,
            //     currentStreak: 0,
            //     bestStreak: 0,
            //     games: [
            //         {
            //              date: '',
            //              won: false,
            //              nbAttempts: 6,
            //          }
            //     ],
            // }
        }
    },
    mounted() {

        // Update timer to next word
        setInterval((function () {
            let duration = moment.duration(this.today.clone().endOf('day').diff(moment()))
            this.countdownToNextWord = moment.utc(duration.as('milliseconds')).format('HH:mm:ss')
            if (duration.as('milliseconds') < 0)
                this.countdownToNextWord = '00:00:00'

        }).bind(this), 1000)

        window.addEventListener('keydown', event => {
            if (/^[a-zA-Z]$/.test(event.key)) {
                this.handleKeyClick(event.key.toUpperCase());
            } else if (event.key === 'Enter') {
                this.handleKeyClick(ENTER);
            } else if (event.key === 'Backspace') {
                this.handleKeyClick(BACKSPACE);
            }
        });

        for (let i = 0; i < NB_ATTEMPTS; i++) {
            this.attempts.push([]);
            this.results.push(new Array(5));
        }
        this.getWordOfTheDay();
        this.getSavedData();

        if (localStorage.getItem('sharedLink')) {
            this.sharedLink = JSON.parse(localStorage.getItem('sharedLink'));
        }

        if (localStorage.getItem('colorBlindMode')) {
            this.colorBlindMode = JSON.parse(localStorage.getItem('colorBlindMode'));
        }

        if (localStorage.getItem('hardWords')) {
            this.hardWords = JSON.parse(localStorage.getItem('hardWords'));
        }

        if (localStorage.getItem('keyboard')) {
            this.keyboard = JSON.parse(localStorage.getItem('keyboard'));
        }
    },
    watch: {
        sharedLink() {
            localStorage.setItem('sharedLink', JSON.stringify(this.sharedLink));
        },
        colorBlindMode() {
            localStorage.setItem('colorBlindMode', JSON.stringify(this.colorBlindMode));
        },
        keyboard() {
            localStorage.setItem('keyboard', JSON.stringify(this.keyboard));
        },
        hardWords() {
            localStorage.setItem('hardWords', JSON.stringify(this.hardWords));
            this.getWordOfTheDay();
        },
    },
    methods: {
        async getWordOfTheDay() {
            const formatedDate = this.today.format('YYYY-M-D');
            const seed = seedrandom(formatedDate);
            const random = seed();
            if (this.hardWords) {
                this.wordOfTheDay = this.extwords[Math.floor(random * (this.words.indexOf('அங்காடி') + 1))];
            } else {
                this.wordOfTheDay = this.words[Math.floor(random * (this.words.indexOf('அங்காடி') + 1))];
            }
            this.baseWordOfTheDay = this.convertToBaseLetters(this.wordOfTheDay)
        },
        getSavedData() {
            if (localStorage.getItem('lastSave')) {
                const lastSave = localStorage.getItem('lastSave');
                if (lastSave === this.today.format('YYYY-M-D')) {
                    if (localStorage.getItem('attempts')) {
                        this.attempts = JSON.parse(localStorage.getItem('attempts'));
                    }
                    if (localStorage.getItem('results')) {
                        this.results = JSON.parse(localStorage.getItem('results'));
                    }
                    if (localStorage.getItem('currentAttempt')) {
                        this.currentAttempt = JSON.parse(localStorage.getItem('currentAttempt'));
                    }
                    if (localStorage.getItem('correctLetters')) {
                        this.correctLetters = JSON.parse(localStorage.getItem('correctLetters'));
                    }
                    if (localStorage.getItem('partialLetters')) {
                        this.partialLetters = JSON.parse(localStorage.getItem('partialLetters'));
                    }
                    if (localStorage.getItem('incorrectLetters')) {
                        this.incorrectLetters = JSON.parse(localStorage.getItem('incorrectLetters'));
                    }
                    if (localStorage.getItem('won')) {
                        this.won = JSON.parse(localStorage.getItem('won'));
                    }
                    if (localStorage.getItem('finished')) {
                        this.finished = JSON.parse(localStorage.getItem('finished'));
                    }
                    if (localStorage.getItem('userResults')) {
                        this.userResults = JSON.parse(localStorage.getItem('userResults'));
                    }
                } else {
                    this.reset();
                }
            }
        },
        reset() {
            localStorage.setItem('attempts', JSON.stringify(this.attempts));
            localStorage.setItem('results', JSON.stringify(this.results));
            localStorage.setItem('currentAttempt', JSON.stringify(this.currentAttempt));
            localStorage.setItem('correctLetters', JSON.stringify(this.correctLetters));
            localStorage.setItem('partialLetters', JSON.stringify(this.partialLetters));
            localStorage.setItem('incorrectLetters', JSON.stringify(this.incorrectLetters));
            localStorage.setItem('won', JSON.stringify(this.won));
            localStorage.setItem('finished', JSON.stringify(this.finished));
            let yesterday = moment().subtract(1, 'day')
            if (localStorage.getItem('lastSave') === yesterday.format('YYYY-M-D')) {
                this.isStreak = true;
            }
            localStorage.setItem('lastSave', this.today.format('YYYY-M-D'));
            if (localStorage.getItem('userResults')) {
                this.userResults = JSON.parse(localStorage.getItem('userResults'));
            }
        },
        getKeyColor(key) {
            if (this.correctLetters.includes(key)) {
                return 'correct';
            } else if (this.partialLetters.includes(key)) {
                return 'partial';
            } else if (this.incorrectLetters.includes(key)) {
                return 'incorrect';
            } else {
                return '';
            }
        },
        handleKeyClick(key) {
            localStorage.setItem('lastSave', this.today.format('YYYY-M-D'));
            this.animateLetter = true;
            this.error = '';
            if (key === ENTER) {
                this.verifyWord(this.attempts[this.currentAttempt - 1]);
            } else if (key === BACKSPACE) {
                if(!this.userResults.games.find((game) => {
                    return game.date === this.today.format('YYYY-M-D');
                })) {
                    this.attempts[this.currentAttempt - 1].pop();
                }
            } else if (this.attempts[this.currentAttempt - 1].length <= NB_LETTERS) {
                let uyir_index = uyir.indexOf(key)
                let changed = false
                let num_chars = this.attempts[this.currentAttempt - 1].length
                if (uyir_index > 0) {
                    // a uyir ezhuthu is pressed
                    if (num_chars != 0) {
                        // check if previous letter is mei yezhuthu
                        let prev_char = this.attempts[this.currentAttempt - 1][num_chars - 1]
                        if (mei.includes(prev_char)) {
                            // change previous letter to appropriate uyirmei ezhuthu
                            this.attempts[this.currentAttempt - 1][num_chars - 1] = uyirmei_table[prev_char][uyir_index]
                            changed = true
                        }
                    }
                }

                if (!changed && num_chars < NB_LETTERS) {
                    this.attempts[this.currentAttempt - 1].push(key);
                }
            }
            localStorage.setItem('attempts', JSON.stringify(this.attempts));
            this.$forceUpdate();
        },
        verifyWord(attempt) {
            if (attempt.length === NB_LETTERS) {
                if (this.words.includes(attempt.join('')) || playableWords.includes(attempt.join(''))) {
                    this.verifyLetters(attempt);
                } else {
                    this.error = 'வார்த்தை அகராதியில் இல்லை';
                    window.setTimeout(() => {
                        this.error = '';
                    }, 1000);
                }
            } else {
                this.error = NB_LETTERS + ' எழுத்துக்கள் வேண்டும்!';
                window.setTimeout(() => {
                    this.error = '';
                }, 1000);
            }
        },
        verifyLetters(attempt) {
            let wordToGuess = this.splitTamilLetters(this.wordOfTheDay);
            let currentResult = this.results[this.currentAttempt - 1];
            
            attempt.forEach((letter, index) => {
                const baseLetter = this.getBaseLetter(letter);
                if (wordToGuess[index] === letter) {
                    currentResult[index] = 'correct';
                    wordToGuess[index] = '*';
                    if (!this.correctLetters.includes(baseLetter)) {
                        this.correctLetters.push(baseLetter);
                    }
                }
            });

            attempt.forEach((letter, index) => {
                const baseLetter = this.getBaseLetter(letter);
                if (currentResult[index] !== 'correct') {
                    if (wordToGuess.includes(letter)) {
                        let otherIndex = wordToGuess.indexOf(letter);
                        currentResult[index] = 'partial';
                        wordToGuess[otherIndex] = '*';
                        if (!this.partialLetters.includes(baseLetter)) {
                            this.partialLetters.push(baseLetter);
                        }
                    } else if (this.baseWordOfTheDay.includes(baseLetter)) {
                        let otherIndex = this.baseWordOfTheDay.indexOf(baseLetter);
                        currentResult[index] = 'partialmei';
                        wordToGuess[otherIndex] = '*';
                        if (!this.partialLetters.includes(baseLetter)) {
                            this.partialLetters.push(baseLetter);
                        }
                    } else {
                        currentResult[index] = 'incorrect';
                        if (!this.incorrectLetters.includes(baseLetter)) {
                            this.incorrectLetters.push(baseLetter);
                        }
                    }
                }
            });
            localStorage.setItem('results', JSON.stringify(this.results));
            localStorage.setItem('correctLetters', JSON.stringify(this.correctLetters));
            localStorage.setItem('partialLetters', JSON.stringify(this.partialLetters));
            localStorage.setItem('incorrectLetters', JSON.stringify(this.incorrectLetters));
            if (attempt.join('') === this.wordOfTheDay) {
                this.won = true;
                this.finished = true;
                this.getStats();
            } else {
                this.currentAttempt++;
                if (this.currentAttempt > NB_ATTEMPTS) {
                    this.finished = true;
                    this.getStats();
                }
            }
            localStorage.setItem('currentAttempt', JSON.stringify(this.currentAttempt));
            localStorage.setItem('won', JSON.stringify(this.won));
            localStorage.setItem('finished', JSON.stringify(this.finished));
        },
        getStats() {
            if(!this.userResults.games.find((game) => {
                return game.date === this.today.format('YYYY-M-D');
            })) {
                this.userResults.nbGames++;
                this.userResults.nbWins += this.won ? 1 : 0;
                this.userResults.currentStreak = this.isStreak && this.won ? this.userResults.currentStreak + 1 : 1;
                if (this.userResults.currentStreak > this.userResults.bestStreak) {
                    this.userResults.bestStreak = this.userResults.currentStreak;
                }
                this.userResults.games.push({
                    date: this.today.format('YYYY-M-D'),
                    won: this.won,
                    nbAttempts: this.currentAttempt,
                });
                localStorage.setItem('userResults', JSON.stringify(this.userResults));
            }
            window.setTimeout(() => { this.statsOpened = true }, 2000);
        },
        getAttemptStat(attemptNumber) {
            let iteration = 0;
            this.userResults.games.forEach((game) => {
                if (game.nbAttempts === attemptNumber) {
                    iteration++;
                }
            });
            return iteration;
        },
        getAttemptStatPercent(attemptNumber) {
            if (this.getAttemptStat(attemptNumber) === 0) {
                return 0;
            }
            let attemptPercent = Math.round((this.getAttemptStat(attemptNumber) / this.userResults.nbGames) * 100);
            this.bestAttemptPercent = attemptPercent > this.bestAttemptPercent ? attemptPercent : this.bestAttemptPercent;
            return attemptPercent;
        },
        getWordID() {
            return this.today.clone().startOf('day').diff(moment("2022-01-24T00:00:00"), 'days') + 1
        },
        share() {
            const title = `சொல்லி #${this.getWordID()} ${this.currentAttempt <= NB_ATTEMPTS ? this.currentAttempt : '💀' }/${NB_ATTEMPTS}\n\n`;
            let schema = this.results.slice(0, this.currentAttempt).map((result) => {
                return result.map((letter) => {
                    if (letter === 'correct') {
                        return '🟩';
                    } else if (letter === 'partial') {
                        return '🟨';
                    } else {
                        return '⬛';
                    }
                }).join('');
            }).join('\n');
            let sharedContent = title + schema;

            navigator.clipboard.writeText(sharedContent);
            this.resultsCopied = true;
        },
        getBaseLetter(letter){
            for (const [key, value] of Object.entries(uyirmei_table)) {
                if (value.includes(letter)) {
                    return key;
                }
            }

            return letter
        },
        splitTamilLetters(word) {
            let tamilSplit = [];
            let diacritics = {'\u0B82':true,'\u0BBE':true, '\u0BBF':true, 
                '\u0BC0':true, '\u0BC1':true, '\u0BC2':true, '\u0BC6':true, 
                '\u0BC7':true, '\u0BC8':true, '\u0BCA':true, '\u0BCB':true, 
                '\u0BCC':true, '\u0BCD':true, '\u0BD7':true};
            let wordSplit = word.split('');
            for(let i = 0; i != wordSplit.length; ++i){
                let ch = wordSplit[i];
                diacritics[ch] ? (tamilSplit[tamilSplit.length - 1] += ch) : tamilSplit.push(ch);
            }

            return tamilSplit;
        },
        convertToBaseLetters(word) {
            let tamilSplit = this.splitTamilLetters(word)
            for (let i = 0; i < tamilSplit.length; i++){
                tamilSplit[i] = this.getBaseLetter(tamilSplit[i])
            }

            return tamilSplit
        }
    }
}
</script>

<style lang="sass" scoped>
#game
    max-width: 500px
    width: 100%
    height: 100%
    overflow: hidden
    display: flex
    flex-direction: column
    background: #121213
    header
        padding: 6px 0
        border-bottom: 1px solid #919191
        width: 100%
        height: 5%
        display: flex
        align-items: center
        justify-content: space-between
        @media (max-width: 500px)
            padding: 0 12px
            box-sizing: border-box
            @media (max-width: 380px)
                h1
                    font-size: 1.5rem
                .header-right, .header-left
                    width: 50px !important
                    .icon
                        width: 20px
                        height: 20px
        h1
            text-transform: uppercase
        .header-right
            display: flex
            width: 75px
            justify-content: space-between
        .header-left 
            width: 75px
        .icon
            width: 24px
            height: 24px
            cursor: pointer
            svg
                path
                    fill: #919191
            &.help
                width: 28px
                height: 28px
                svg
                    path
                        fill: none
                        stroke: #919191
                    circle
                        fill: #919191
    main
        height: 95%
        display: flex
        flex-direction: column
        align-items: center
        justify-content: space-between
        box-sizing: border-box
        position: relative
        .fade-enter-active, .fade-leave-active
            transition: opacity .5s
        .fade-enter, .fade-leave-to
            opacity: 0
        .fadeup-enter-active, .fade-leave-active
            transition: opacity .5s
        .fadeup-enter, .fade-leave-to
            opacity: 0
            transform: translateY(10px)
        .error
            top: 20px
            margin-top: 6px
            position: absolute
            background: #ebebeb
            color: #121213
            padding: 0.5em 1em
            border-radius: 0.5em
            font-size: 18px
            font-weight: bold
            z-index: 2
        .grid
            margin-top: auto
            margin-bottom: auto
            .attempt
                display: flex
                animation-duration: 0.3s
                &.shake
                    animation-name: shake
        .keyboard
            margin-bottom: 12px
        .help-modal
            position: fixed
            width: 100vw
            height: 100vh
            display: flex
            justify-content: center
            align-items: center
            background: rgba(0, 0, 0, 0.5)
            top: 0
            left: 0
            z-index: 10
            .help-modal-content
                max-width: 450px
                width: 90%
                min-height: 420px
                max-height: 100%
                overflow-y: auto
                background: #121213
                border-radius: 8px
                padding: 12px
                display: flex
                flex-direction: column
                align-items: center
                font-size: 14px
                position: relative
                .close-btn
                    align-self: flex-end
                    cursor: pointer
                h2
                    text-transform: uppercase
                    padding-bottom: 12px
                    border-bottom: 1px solid #919191
                p
                    margin-top: 12px
                    text-align: left
                    a
                        color: white
                        text-decoration: none
                .help-exemple
                    border-top: 1px solid #919191
                    border-bottom: 1px solid #919191
                    margin-top: 12px
                    padding-bottom: 12px
                    .help-word
                        display: flex
                        margin-top: 12px
                        .help-letter-container
                            width: 36px
                            height: 36px
                            border: 2px solid #919191
                            box-sizing: border-box
                            margin: 2px
                            display: flex
                            align-items: center
                            justify-content: center
                            font-size: 20px
                            font-weight: bold
                            color: white
                            &.correct
                                border: none
                                background: #538D4E
                                &.color-blind
                                    background: #F5793A
                            &.partial
                                border: none
                                background: #B59E3B
                                &.color-blind
                                    background: #85C0F9
                            &.incorrect
                                border: none
                                background: #3A3A3C
                            &.partialmei
                                border: none
                                background: #957D95 
                                &.color-blind
                                    background: #D81E5B
                    p
                        span
                            font-weight: bold  
        .endgame-modal
            position: fixed
            width: 100vw
            height: 100vh
            display: flex
            justify-content: center
            align-items: center
            background: rgba(0, 0, 0, 0.5)
            top: 0
            left: 0
            z-index: 10
            .endgame-modal-content
                max-width: 450px
                width: 90%
                min-height: 420px
                max-height: 100%
                overflow-y: auto
                background: #121213
                border-radius: 8px
                padding: 12px
                display: flex
                flex-direction: column
                align-items: center
                h2
                    font-size: 18px
                    text-transform: uppercase
                    font-weight: bold
                .close-btn
                    align-self: flex-end
                    cursor: pointer
                .stats
                    .stats-content
                        display: flex
                        .stats-item
                            margin-top: 12px
                            width: 70px
                            .stat-item-figure
                                font-size: 30px
                                font-weight: bold
                            .stat-item-label
                                font-size: 12px
                .graph
                    margin-top: 18px
                    width: 100%
                    display: flex
                    flex-direction: column
                    align-items: center
                    .graph-content
                        margin-top: 12px
                        width: 80%
                        display: flex
                        flex-direction: column
                        .graph-item
                            margin-top: 6px
                            width: 100%
                            display: flex
                            font-size: 14px
                            .attempt-number
                                width: 20px
                                height: 20px
                                display: flex
                                align-items: center
                                justify-content: center
                            .attempt-skull
                                width: 20px
                                height: 20px
                                display: flex
                                align-items: center
                            .attempt-stat
                                height: 100%
                                width: 100%
                                .attempt-bar
                                    margin-left: 6px
                                    height: 100%
                                    background: #3A3A3C
                                    color: white
                                    display: flex
                                    box-sizing: border-box
                                    padding: 0 6px
                                    justify-content: flex-end
                                    align-items: center
                                    min-width: 20px
                                    &.best
                                        background: #538D4E
                .soluce
                    margin-top: 24px
                    display: flex
                    strong
                        padding-left: 4px
                        display: block
                    .definition-icon
                        svg
                            width: 1em
                            height: 1em
                            margin-left: 8px
                            fill: #919191
                .modal-footer
                    display: flex
                    width: 100%
                    max-width: 400px
                    justify-content: space-around
                    align-items: center
                    margin-top: 24px
                    .next-in
                        display: flex
                        flex-direction: column
                        .time
                            font-size: 24px
                            color: darken(white, 20%)
                    @media (max-width: 400px)
                        margin-top: 12px
                        .next-in
                            font-size: 12px
                            .time
                                font-size: 20px
                    .separator
                        width: 1px
                        height: 36px
                        background: #919191
                    .share
                        .share-button
                            display: flex
                            align-items: center
                            justify-content: space-around
                            background: #538D4E
                            border: none
                            padding: 0.5em 1em
                            border-radius: 8px
                            cursor: pointer
                            width: 136px
                            p
                                text-transform: uppercase
                                font-weight: bold
                                font-size: 14px
                                color: white
                            svg
                                width: 24px
                                height: 24px
                                margin-left: 8px
                                path
                                    fill: white
        .settings-modal
            position: fixed
            width: 100vw
            height: 100vh
            display: flex
            justify-content: center
            align-items: center
            background: rgba(0, 0, 0, 0.5)
            top: 0
            left: 0
            z-index: 10
            .settings-modal-content
                max-width: 450px
                width: 90%
                min-height: 420px
                max-height: 100%
                overflow-y: auto
                background: #121213
                border-radius: 8px
                padding: 12px
                display: flex
                flex-direction: column
                align-items: center
                .close-btn
                    align-self: flex-end
                    cursor: pointer
                h2
                    text-transform: uppercase
                    padding-bottom: 12px
                    border-bottom: 1px solid #919191
                .settings-content
                    width: 100%
                    .settings-item
                        width: 100%
                        padding: 12px 0
                        border-bottom: 1px solid #919191
                        &.setting-toggle
                            display: flex
                            justify-content: space-between
                            align-items: center
                            .toggle-button
                                background: #3A3A3C
                                width: 36px
                                height: 1.2em
                                border-radius: 1.2em
                                box-sizing: border-box
                                cursor: pointer
                                transition: all 0.3s
                                position: relative
                                .toggle
                                    background: #919191
                                    height: calc(100% - 4px)
                                    width: 45%
                                    border-radius: 1.2em
                                    position: absolute
                                    left: 2px
                                    top: 1px
                                    transition: all 0.3s
                                &.activated
                                    background: #538D4E
                                    .toggle
                                        background: white
                                        left: 50%
                        &.setting-button
                            display: flex
                            justify-content: space-between
                            align-items: center
                            button
                                background: transparent
                                cursor: pointer
                                color: #919191
                                border: 1px solid #919191
                                padding: 0.5em 1em
                                &.first
                                    border-radius: 8px 0 0 8px
                                &.last
                                    border-radius: 0 8px 8px 0
                                &.selected
                                    background: #919191
                                    color: white
                                    font-weight: bold
                            @media (max-width: 375px)
                                button
                                    font-size: 12px
                                @media (max-width: 320px)
                                    button
                                        font-size: 10px
                                    @media (max-width: 300px)
                                        button
                                            padding: 0.3em
                        &.credits
                            h3
                                text-align: left
                            p
                                text-align: left
                                margin-top: 6px
                                font-size: 12px
                                line-height: 16px
                                a
                                    color: white
                                    text-decoration: none

@keyframes shake
    0%
        transform: translateX(0)
    20%
        transform: translateX(-10px)
    40%
        transform: translateX(10px)
    60%
        transform: translateX(-10px)
    80%
        transform: translateX(10px)
    100%
        transform: translateX(0)
</style>
