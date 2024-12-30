import { initCharts, setChartData } from './charts.js';
import { initMap, updateMap } from './map.js';
import { fillLegend } from './legend.js';

const searchbar = document.querySelector('.searchbar');
const categoryDropdown = document.querySelector('.form-select');
const hintContainer = document.querySelector('.search-hints');

//Searchbar / hint click flag for emptying hint container
let isClickEventPending = false;

//Global index for indicating which hint should be highlighted
let highlightedHintIndex = -1;

//First search occurence flag
let hasSearched = false;

document.addEventListener('DOMContentLoaded', init);

function init() {   
    setSearchbarListeners();
    setCategoryDropdownListener();
    setYearInFooter();
    setArrowGifPageScroll();

    initCharts();
    initMap();
}

function setYearInFooter() {
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();

    const yearSpan = $('footer span');
    
    yearSpan.text(currentYear);
}

function setArrowGifPageScroll() {
    $('.scroll-gif').on('click', function() {
        const aboutHeading = $("h2:contains('About')");    
        const y = aboutHeading.offset().top - 24;
    
        $('html, body').animate({
            scrollTop: y
        }, 1000);
    });
}

function setCategoryDropdownListener() {
    $('.form-select').on('change', function() {
        emptyHintsContainer();
        emptySearchbar();
        searchbar.focus();
    });
}

function setSearchbarListeners() {
    //Update hints on input
    searchbar.addEventListener('input', getHints);
    
    //Resets the highlighted hint when input changes
    searchbar.addEventListener('input', resetHiglightedHintIndex)

    //Listen for arrowkeys
    searchbar.addEventListener('keydown', hintContainerKeyControls);

    //Prevents the caret from shifting place when using arrow keys to nav hint container
    searchbar.addEventListener('keydown', function(event) {
        if(event.key == 'ArrowUp' || event.key == 'ArrowDown') {
            event.preventDefault();
        }
    });

    //Emptying the hints container when search bar looses focus.
    searchbar.addEventListener('blur', function() {
        setTimeout(() => {
            if (!isClickEventPending) {
                emptyHintsContainer();
            }
        }, 100);
    });

    //Resetting the pending flag when searchbar regains focus.
    searchbar.addEventListener('focus', function () {
        isClickEventPending = false;
    });
}

function hintContainerKeyControls(event) {
    const hints = hintContainer.querySelectorAll('.hint');

    if (event.key === 'ArrowUp' && highlightedHintIndex > 0) {
        updateHintHighlight(--highlightedHintIndex);
    } else if (event.key === 'ArrowDown' && highlightedHintIndex < hints.length - 1) {
        updateHintHighlight(++highlightedHintIndex);
    } else if (event.key === 'Enter') {
        if(highlightedHintIndex != -1) {
            const higlightedHint = hints[highlightedHintIndex];
            getResults(higlightedHint);
        }
    }
}

function updateHintHighlight(index) {
    const hints = Array.from(hintContainer.querySelectorAll('.hint'));
    
    highlightedHintIndex = index;

    // Remove 'highlight' class from all hints
    hints.forEach((item) => item.classList.remove('highlight'));
    
    // Add 'highlight' class to the selected hint
    hints[index].classList.add('highlight');
}

function makeHint(data, category, index) {
    const hint = document.createElement('div');
    hint.classList.add('hint');    
    
    hint.dataset.id = data.id;
    hint.dataset.category = category;
    hint.textContent = data.body;
    
    hint.addEventListener('click', () => {
        isClickEventPending = true;
        getResults(hint);
    });

    hint.addEventListener('mouseover', () => {
        updateHintHighlight(index);
    });
    
    return hint;
} 

function updateResultsLabel(text, category) {
    const prefix = getPrefixForCategory(category);
    
    $('.result-label-span').text(prefix + ' ' + text);
}

function getPrefixForCategory(category_id) {
    switch (category_id) {
        case '3':
            return 'gmina'
        case '4':
            return 'powiat'
        case '5':
            return 'województwo'
        default:
            return '';
    }
}

async function getLocationCoordinates(placename, category) {
    const response = await fetch(`/location?placename=${placename}&category=${category}`);
    const data = await response.json();

    updateMap(data);
}

async function getHints() {
    const keyword = searchbar.value;
    const category = categoryDropdown.value;

    if (keyword === '') {
        emptyHintsContainer();
        return;
    }

    const response = await fetch(`/hints?keyword=${keyword}&category=${category}`);
    const data = await response.json();

    emptyHintsContainer();

    if (data.length === 0) {
        emptyHintsContainer();
        const newHint = makeHint('No results.', 0, 0);
        hintContainer.append(newHint);
    } else {
        data.forEach(async (item, index) => {
            const newHint = makeHint(item, category, index);
            hintContainer.append(newHint);
        });
    }
}

async function getResults(hint) {
    const id = hint.dataset.id;
    const category = hint.dataset.category;
    const body = hint.textContent;

    getLocationCoordinates(body, category)

    updateResultsLabel(body, category);

    emptyHintsContainer();
    emptySearchbar();
    
    const response = await fetch(`/results?id=${id}&category=${category}`);
    const data = await response.json();

    if(!hasSearched) {
        let appDivLabel = $("h2:contains('App')");
        let marginOffset = parseInt(appDivLabel.css('margin-top')) || 0;
        
        $('html, body').animate({
            scrollTop: appDivLabel.offset().top - marginOffset
        }, 1000);
        
        $(".results-div").slideDown(1000);
        hasSearched = true;
    }

    fillLegend(data);
    setChartData(data);
}

function emptyHintsContainer() {
    hintContainer.innerHTML = '';
}

function emptySearchbar() {
    searchbar.value = '';
}

function resetHiglightedHintIndex() {
    highlightedHintIndex = -1;
}