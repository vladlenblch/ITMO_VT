const CONST = 100;

let websocket = null;
let gazePoint = { x: 200, y: 150 };
let isConnected = false;

function connectWebSocket() {
	try {
		websocket = new WebSocket('ws://localhost:8765');
		
		websocket.onopen = function(event) {
			console.log('WebSocket соединение установлено');
			isConnected = true;
			updateConnectionStatus('подключено к eye tracker');
			drawCoordinateSystem();
		};
		
		websocket.onmessage = function(event) {
			try {
				const data = JSON.parse(event.data);
				handleWebSocketMessage(data);
			} catch (e) {
				console.error('ошибка парсинга WebSocket сообщения:', e);
			}
		};
		
		websocket.onclose = function(event) {
			console.log('WebSocket соединение закрыто');
			isConnected = false;
			updateConnectionStatus('отключено от eye tracker');
			
			setTimeout(connectWebSocket, 3000);
		};
		
		websocket.onerror = function(error) {
			console.error('WebSocket ошибка:', error);
			updateConnectionStatus('ошибка подключения');
		};
	} catch (e) {
		console.error('не удалось создать WebSocket соединение:', e);
		updateConnectionStatus('WebSocket недоступен');
	}
}

function handleWebSocketMessage(data) {
	if (window.__dbg) {
		console.log('[WS]', data);
	}
	switch (data.type) {
		case 'gaze_update':
			gazePoint.x = data.x;
			gazePoint.y = data.y;
			drawCoordinateSystem();
			break;
			
		case 'connection':
			console.log('статус подключения:', data.message);
			updateConnectionStatus('реальный eye tracker подключен');
			gazePoint.x = 200;
            gazePoint.y = 150;
            drawCoordinateSystem();
			break;
			
		case 'pong':
			console.log('Pong получен');
			break;
	}
}

function updateConnectionStatus(message) {
	console.log('статус:', message);
}

function drawCoordinateSystem() {
	const canvas = document.getElementById('coordinateCanvas');
	const ctx = canvas.getContext('2d');
	
	const rect = canvas.getBoundingClientRect();
	canvas.width = rect.width;
	canvas.height = rect.height;
	
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	
	const centerX = canvas.width / 2;
	const centerY = canvas.height / 2;
	
	ctx.strokeStyle = '#666';
	ctx.lineWidth = 2;
	ctx.beginPath();
	ctx.moveTo(centerX, 0);
	ctx.lineTo(centerX, canvas.height);
	ctx.moveTo(0, centerY);
	ctx.lineTo(canvas.width, centerY);
	ctx.stroke();
	
	drawShapes(ctx, centerX, centerY);
	
    drawGazePoint(ctx);
}

function drawShapes(ctx, centerX, centerY) {
	ctx.fillStyle = 'rgba(100, 150, 255, 0.4)';
	ctx.strokeStyle = '#4a9eff';
	ctx.lineWidth = 2;
	
	ctx.beginPath();
	ctx.moveTo(centerX, centerY);
	ctx.lineTo(centerX + CONST, centerY);
	ctx.lineTo(centerX, centerY - CONST/2);
	ctx.closePath();
	ctx.fill();
	ctx.stroke();
	
	ctx.beginPath();
	ctx.arc(centerX, centerY, CONST, 0, Math.PI/2, false);
	ctx.lineTo(centerX, centerY);
	ctx.closePath();
	ctx.fill();
	ctx.stroke();
	
	ctx.beginPath();
	ctx.rect(centerX - CONST, centerY, CONST, CONST/2);
	ctx.fill();
	ctx.stroke();
}

window.addEventListener('DOMContentLoaded', async () => {
	if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
		try {
			const stream = await navigator.mediaDevices.getUserMedia({ video: true });
			for (const track of stream.getTracks()) track.stop();
		} catch (err) {
			console.warn('нет доступа к веб-камере:', err.message);
		}
	}

	drawCoordinateSystem();
	connectWebSocket();
	if (window.__dbg) console.log('[INIT] WS connecting');
	window.addEventListener('resize', () => {
		drawCoordinateSystem();
	});
});

function drawGazePoint(ctx) {
	ctx.save();
	
	ctx.fillStyle = '#ff0000';
	ctx.beginPath();
	ctx.arc(gazePoint.x, gazePoint.y, 3, 0, 2 * Math.PI);
	ctx.fill();
	
	ctx.strokeStyle = '#ffffff';
	ctx.lineWidth = 2;
	ctx.beginPath();
	ctx.arc(gazePoint.x, gazePoint.y, 5, 0, 2 * Math.PI);
	ctx.stroke();
	
	ctx.fillStyle = isConnected ? '#00ff00' : '#ff0000';
	ctx.font = '12px Arial';
	ctx.textAlign = 'left';
	ctx.fillText(isConnected ? 'Eye Tracker: ON' : 'Eye Tracker: OFF', 10, 20);
	if (window.__dbg) {
		ctx.fillText(`gaze=(${Math.round(gazePoint.x)}, ${Math.round(gazePoint.y)})`, 10, 36);
	}
	
	ctx.restore();
}

function checkPointInArea(x, y) {
	const canvas = document.getElementById('coordinateCanvas');
	const centerX = canvas.width / 2;
	const centerY = canvas.height / 2;
	
	const relX = x - centerX;
	const relY = y - centerY;
	
	if (relX >= 0 && relY <= 0) {
		if (relX <= CONST && relY >= -CONST/2 && relX + 2 * Math.abs(relY) <= CONST) {
			return true;
		}
	}
	
	if (relX >= 0 && relY >= 0) {
		const distance = Math.sqrt(relX * relX + relY * relY);
		if (distance <= CONST) {
			return true;
		}
	}
	
	if (relX <= 0 && relY >= 0) {
		if (relX >= -CONST && relY <= CONST/2) {
			return true;
		}
	}
	
	return false;
}

function addResultToTable(result, time) {
	const tbody = document.getElementById('resultsTableBody');
	const row = document.createElement('tr');
	
	const timeCell = document.createElement('td');
	timeCell.textContent = time;
	
	const resultCell = document.createElement('td');
	resultCell.textContent = result ? 'Попадание' : 'Промах';
	resultCell.style.color = result ? '#28a745' : '#dc3545';
	resultCell.style.fontWeight = 'bold';
	
	row.appendChild(timeCell);
	row.appendChild(resultCell);
	
	tbody.insertBefore(row, tbody.firstChild);
	
	const maxRows = 20;
	while (tbody.children.length > maxRows) {
		tbody.removeChild(tbody.lastChild);
	}
}

function clearResultsTable() {
	const tbody = document.getElementById('resultsTableBody');
	tbody.innerHTML = '';
}

function simulateDoubleBlink() {
	const result = checkPointInArea(gazePoint.x, gazePoint.y);
	const time = new Date().toLocaleTimeString();
	addResultToTable(result, time);
	console.log(`Выстрел: ${result ? 'Попадание' : 'Промах'} в точке (${gazePoint.x}, ${gazePoint.y})`);
}

document.addEventListener('keydown', (event) => {
	if (event.code === 'Space') {
		event.preventDefault();
		simulateDoubleBlink();
		console.log('выстрел по пробелу');
	}
});
