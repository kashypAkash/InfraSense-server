DELIMITER |

CREATE EVENT `InfraSense`.sensorData
ON SCHEDULE EVERY 15 SECOND
STARTS CURRENT_TIMESTAMP
ON COMPLETION PRESERVE
DO 
BEGIN
DECLARE n INT DEFAULT 0;
DECLARE i INT DEFAULT 0;
SELECT COUNT(*) FROM `InfraSense`.sensor WHERE Status='running' INTO n;
SET i=0;
WHILE i<n DO
	#loop to insert
	INSERT INTO `InfraSense`.sensordata (SensorId, Data, Timestamp)
	VALUES(
    (Select s.Sensorid 
	from `InfraSense`.sensor s 
	where s.id = i + 1), 
    (SELECT 
    CASE 
    WHEN u.SensorType = 'Temperature Sensor' THEN ROUND(RAND()*(80-32)+32,2)
    WHEN u.SensorType = 'Pressure Sensor' THEN ROUND(RAND()*(850-650)+650,2)
    WHEN u.SensorType = 'Wind Sensor' THEN ROUND(RAND()*(20-5)+5,2)
    WHEN u.SensorType = 'Humidity Sensor' THEN ROUND(RAND()*(50-40)+40,2)
    END
    FROM `infraSense-dev`.sensor u
    WHERE u.id = i+1),
    CURRENT_TIMESTAMP
    );
	SET i = i + 1;
END WHILE;
END |

DELIMITER ;
