const legendContainer = document.querySelector('.legend-div');

function makeLegendItem(data) {
    const legendItem = document.createElement('div');
    legendItem.classList.add('legend-item');

    const img = document.createElement('img');
    img.setAttribute('src', data.party_img_uri);
    img.classList.add('party-img')

    const partyName = document.createElement('p');
    partyName.textContent = data.name;

    const percentageBarWrapper = document.createElement('div');

    const percentage = document.createElement('p');
    percentage.textContent = data.votes_percentage + '%';

    const percentageBar = document.createElement('div');
    percentageBar.classList.add('.progress-bar')
    percentageBar.style.width = data.votes_percentage + '%';
    percentageBar.style.backgroundColor = data.color;

    percentageBarWrapper.append(partyName, percentageBar, percentage)
    
    legendItem.append(img, percentageBarWrapper);

    return legendItem;
}

export function fillLegend(data) {
    legendContainer.innerHTML = '';

    data.forEach(item => {
        let legendItem = makeLegendItem(item)
        legendContainer.append(legendItem)
    });
}