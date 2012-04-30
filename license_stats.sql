SELECT 
    license_type, 
    count(id) as count, 
    avg(commits) as commits, 
    avg(issues) as issues, 
    avg(collaborators) as collaborators, 
    avg(watchers) as watchers,
    avg(forks) as forks,
    avg(datediff(now(), created)) as age
FROM 
    repos
WHERE 
    error is null 
GROUP BY 
    license_type 