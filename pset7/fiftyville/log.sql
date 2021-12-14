-- Keep a log of any SQL queries you execute as you solve the mystery.
--left courthouse in car and rang someone to buy them a plane ticket for <1min


select * from crime_scene_reports where year = 2020 and day = 28 and month = 7;
-- ID = 295

select * from interviews where year = 2020 and day = 28 and month = 7;
--seeing what relevant interviews there were

select people.id, people.name from people
join phone_calls on phone_calls.receiver = people.phone_number
where phone_calls.year = 2020 and phone_calls.day = 28 and phone_calls.month = 7
and
select * from airports where city = "Fiftyville";
--to find fiftyville id 8

select * from flights where origin_airport_id=8 and year = 2020 and day = 29 and month = 7
order by hour asc;
--id 36

SELECT DISTINCT name FROM passengers
JOIN people ON people.passport_number = passengers.passport_number
join phone_calls on phone_calls.caller = people.phone_number
join courthouse_security_logs ON courthouse_security_logs.license_plate = people.license_plate
WHERE flight_id = 36 AND
phone_number IN
(
select caller from phone_calls
where year = 2020 and day = 28 and month = 7 and duration < 60
) AND
people.license_plate IN
(
select license_plate from courthouse_security_logs
where year = 2020 and day = 28 and month = 7 and hour = 10 and minute < 25 and activity = 'exit'
) AND
people.id IN
(
SELECT person_id from bank_accounts
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE
atm_transactions.atm_location = "Fifer Street" and
atm_transactions.year = 2020 and atm_transactions.day = 28 and
atm_transactions.month = 7 and atm_transactions.transaction_type = 'withdraw'
);
--used this to narrow it down to Ernest(686048) (367) 555-5533

select * from crime_scene_reports
where year = 2020 and day = 28 and month = 7;
-- used to get time of the crime

SELECT * FROM flights
WHERE id = 36;
-- to find dest (4) heathrow

select * from phone_calls
where year = 2020 and day = 28 and month = 7 and caller = "(367) 555-5533";
--to find outgoing call from E


select * from people
where phone_number = "(375) 555-8161";
