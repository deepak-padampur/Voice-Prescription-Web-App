//creating a doctor function constructor
let nameDoctor=[ 'Dr.  Asha Latha Hegde' , 'Dr.  Parimala' , 'Dr.  Ekta' ];
let image = [ 'https://assets.mfine.co/api/contentservice/attachments/downloadFromDb?fileName=Dr. Asha Latha Hedge.jpg/w_95,h_110' , 'https://assets.mfine.co/api/contentservice/attachments/downloadFromDb?fileName=Dr. Parimala Devi.jpg/w_95,h_110' , 'https://assets.mfine.co/api/contentservice/attachments/downloadFromDb?fileName=Dr.Ekta-Dhawale.jpg/w_95,h_110'];
let department = [ 'Gynaecologist' , 'Gynaecologist' , 'Gynaecologist'];
let degree=['MBBS, MD - Obstetrics & Gynaecology' , 'MD - Obstetrics & Gynaecology,FICS,DGO,MBBS' , 'MBBS, MD - Obstetrics & Gynaecology'];
let Doctor=function(name,image,department,degree){
    this.name=name;
    this.image=image;
    this.department=department;
    this.degree=degree;

}
// console.info(nameDoctor);
// console.info(image);
// console.info(department);
// console.info(degree);

// let Doctor1=new Doctor(nameDoctor[0],image[0],department[0],degree[0]);
// console.log('Doctor1='+Doctor1);
let Profile=[];
for(let i=0;i<=nameDoctor.length;i++){
   
    let instance=new Doctor(nameDoctor[i],image[i],department[i],degree[i]);
    Profile.push(instance);
}
console.log("Profile="+Profile);
