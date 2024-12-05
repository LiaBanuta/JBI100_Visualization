import * as XLSX from 'xlsx';

export const processExcelFile = async (file) => {
  const data = await file.arrayBuffer();
  const workbook = XLSX.read(data);
  const worksheet = workbook.Sheets[workbook.SheetNames[0]];
  const jsonData = XLSX.utils.sheet_to_json(worksheet);

  return jsonData.map(row => ({
    year: row['Incident.year'],
    month: row['Incident.month'],
    injury: row['Victim.injury'],
    state: row['State'],
    location: row['Location'],
    latitude: parseFloat(row['Latitude']),
    longitude: parseFloat(row['Longitude']),
    siteCategory: row['Site.category'],
    sharkType: row['Shark.common.name'],
    provoked: row['Provoked/unprovoked'],
    activity: row['Victim.activity']
  }));
};

export const aggregateByYear = (data) => {
  return data.reduce((acc, curr) => {
    const year = curr.year;
    acc[year] = (acc[year] || 0) + 1;
    return acc;
  }, {});
};

export const aggregateByState = (data) => {
  return data.reduce((acc, curr) => {
    const state = curr.state;
    acc[state] = (acc[state] || 0) + 1;
    return acc;
  }, {});
};

export const aggregateByActivity = (data) => {
  return data.reduce((acc, curr) => {
    const activity = curr.activity;
    acc[activity] = (acc[activity] || 0) + 1;
    return acc;
  }, {});
};