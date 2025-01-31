function addForms(brigade = '', departureTime = '', arrivalTime = '', closureTime = '') {
    // новый div для формы
    const brigadeFormDiv = document.createElement('div');
    brigadeFormDiv.className = 'form-container';

    // элементы формы для выбора бригады
    const brigadeLabel = document.createElement('label');
    brigadeLabel.innerText = 'Выберите бригаду:';

    const brigadeSelect = document.createElement('select');
    brigadeSelect.name = 'brigade';

    // опции в выпадающий список из массива brigades
    brigades.forEach(brigadeOption => {
        const option = document.createElement('option');
        option.value = brigadeOption;
        option.innerText = brigadeOption;
        if (brigadeOption === brigade) {
            option.selected = true;
        }
        brigadeSelect.appendChild(option);
    });

    // элементы для ввода времени
    const departureTimeLabel = document.createElement('label');
    departureTimeLabel.innerText = 'Время выезда:';
    const departureTimeInput = document.createElement('input');
    departureTimeInput.type = 'time';
    departureTimeInput.name = 'departure_time';
    departureTimeInput.value = departureTime;

    const arrivalTimeLabel = document.createElement('label');
    arrivalTimeLabel.innerText = 'Время прибытия:';
    const arrivalTimeInput = document.createElement('input');
    arrivalTimeInput.type = 'time';
    arrivalTimeInput.name = 'arrival_time';
    arrivalTimeInput.value = arrivalTime;

    const closureTimeLabel = document.createElement('label');
    closureTimeLabel.innerText = 'Время закрытия вызова:';
    const closureTimeInput = document.createElement('input');
    closureTimeInput.type = 'time';
    closureTimeInput.name = 'closure_time';
    closureTimeInput.value = closureTime;

    // кнопка удаления
    const removeButton = document.createElement('button');
    removeButton.innerText = 'Удалить';
    removeButton.type = 'button';
    removeButton.onclick = function() {
        brigadeFormDiv.remove();
    };

    // добавление элементов в div формы
    brigadeFormDiv.appendChild(brigadeLabel);
    brigadeFormDiv.appendChild(brigadeSelect);
    //brigadeFormDiv.appendChild(document.createElement('br'));
    brigadeFormDiv.appendChild(departureTimeLabel);
    brigadeFormDiv.appendChild(departureTimeInput);
    //brigadeFormDiv.appendChild(document.createElement('br'));
    brigadeFormDiv.appendChild(arrivalTimeLabel);
    brigadeFormDiv.appendChild(arrivalTimeInput);
    //brigadeFormDiv.appendChild(document.createElement('br'));
    brigadeFormDiv.appendChild(closureTimeLabel);
    brigadeFormDiv.appendChild(closureTimeInput);
    //brigadeFormDiv.appendChild(document.createElement('br'));
    brigadeFormDiv.appendChild(removeButton); // Добавляем кнопку удаления


    document.getElementById('form-container').appendChild(brigadeFormDiv);
}
