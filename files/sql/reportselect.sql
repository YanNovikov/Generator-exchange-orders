SELECT Count(DISTINCT p.Id) FROM orders p
UNION
SELECT Count(DISTINCT p.Id) FROM orders p
WHERE p.Id IN (SELECT Id FROM orders WHERE Status LIKE 'New') AND
    p.Id IN (SELECT Id FROM orders WHERE Status LIKE 'To-provider') AND
    (p.Id IN (SELECT Id FROM orders WHERE Status LIKE 'Filled') OR
        p.Id IN (SELECT Id FROM orders WHERE Status LIKE 'Partial-filled') OR
        p.Id IN (SELECT Id FROM orders WHERE Status LIKE 'Reject'))
UNION
SELECT Count(DISTINCT p.Id) FROM orders p
WHERE p.Id IN (SELECT Id FROM orders WHERE Status LIKE 'To-provider') AND
        (p.Id IN (SELECT Id FROM orders WHERE Status LIKE 'Filled') OR
        p.Id IN (SELECT Id FROM orders WHERE Status LIKE 'Partial-filled') OR
        p.Id IN (SELECT Id FROM orders WHERE Status LIKE 'Reject')) OR
        (p.Id IN (SELECT Id FROM orders WHERE Status LIKE 'Filled') OR
        p.Id IN (SELECT Id FROM orders WHERE Status LIKE 'Partial-filled') OR
        p.Id IN (SELECT Id FROM orders WHERE Status LIKE 'Reject'))

