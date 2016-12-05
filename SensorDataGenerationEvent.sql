SET GLOBAL event_scheduler = ON;

#
#	An Event to create new sensor data records for all sensors in interval of 15 seconds
#

DELIMITER |

CREATE EVENT `infraSense-dev`.sensorData
ON SCHEDULE EVERY 15 SECOND
STARTS CURRENT_TIMESTAMP
ON COMPLETION PRESERVE
DO 
BEGIN
DECLARE n INT DEFAULT 0;
DECLARE i INT DEFAULT 0;
SELECT COUNT(*) FROM `infraSense-dev`.sensor WHERE Status='running' INTO n;
SET i=0;
WHILE i<n DO
	#loop to insert
	INSERT INTO `infraSense-dev`.sensordata (SensorId, Data, Timestamp)
	VALUES(
    (Select s.Sensorid 
	from `infraSense-dev`.sensor s 
	where s.id = i + 1), 
    (SELECT 
    CASE 
    WHEN u.SensorType = 'Temperature Sensor' THEN ROUND(RAND()*(80-32)+32,2)
    WHEN u.SensorType = 'Pressure Sensor' THEN ROUND(RAND()*(32-0)+0,2)
    WHEN u.SensorType = 'Oxygen Sensor' THEN ROUND(RAND()*(32-0)+0,2)
    WHEN u.SensorType = 'Salinity Sensor' THEN ROUND(RAND()*(32-0)+0,2)
    END
    FROM `infraSense-dev`.sensor u
    WHERE u.id = i+1),
    CURRENT_TIMESTAMP
    );
	SET i = i + 1;
END WHILE;
END |

DELIMITER ;
