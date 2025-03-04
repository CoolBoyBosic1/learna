document.addEventListener("DOMContentLoaded", function () {
    let selectedSlots = new Set();
    let isMouseDown = false;
    let startSlot = null;

    function toggleSelection(slot) {
        let slotKey = slot.getAttribute('data-day') + '-' + slot.getAttribute('data-hour');

        if (selectedSlots.has(slotKey)) {
            selectedSlots.delete(slotKey);
            slot.classList.remove('selected');
        } else {
            selectedSlots.add(slotKey);
            slot.classList.add('selected');
        }
    }

    document.querySelectorAll('.slot').forEach(slot => {
        slot.addEventListener('mousedown', function (event) {
            isMouseDown = true;
            startSlot = this;
            toggleSelection(this);
            event.preventDefault();
        });

        slot.addEventListener('mouseenter', function () {
            if (isMouseDown) {
                toggleSelection(this);
            }
        });
    });

    document.addEventListener('mouseup', function () {
        isMouseDown = false;
    });

    window.submitTime = function () {
        if (selectedSlots.size === 0) {
            alert("Будь ласка, оберіть хоча б один час!");
            return;
        }

        let selectedData = Array.from(selectedSlots);
        console.log("Обрані слоти:", selectedData);
        alert("Вибрано: " + selectedData.join(", "));
    };
});
