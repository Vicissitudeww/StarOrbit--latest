document.addEventListener('DOMContentLoaded', function(){
  const form = document.getElementById('sched-form');
  if (!form) return;
  form.addEventListener('submit', async function(e){
    // allow normal POST to server for now; this JS can be extended for async UX
  });
});
