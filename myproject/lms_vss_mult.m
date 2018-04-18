function [procent, msqe]=lms_vss_mult(M, frek,th)

% Kako se povikuva funkcijata:
% [brojac,e,w,y]=lms(mu,M,d,th);
%
% Vlezni argumenti:
% mu = step size ili rata na uchenje, dimenzii 1x1
% ovaa konstanta treba da pripagja pomegju 0 i 1/Ex, kade shto Ex e
% 1/R*sum(k=1:R)X(k)^2, kade shto R e brojot na iteracii za da se istrenira filterot
% obichno ova se zamenuva so ocenka za M-te posledni Ex kade shto M e
% dolzhina na filterot
% M = dolzhina na filterot, dim 1x1
% d = vlezen signal
%
% Izlezni argumenti:
% e = grehka vo predviduvanjeto, dim Nx1
% w = konechni tezhini na filterot (koeficienti na filterot so dolzhina M), dim Mx1
% brojac = broi kolku pati se izvrshilo transmisija na podatocite
% y = pretvideni vrednosti za otchituvanjeto

%spored trudot, inicijalnite vrednosti na tezhinite se 0, konkretno toa ni
%e vektor so dolzhina M (dolzhina na filterot)
d = csvread('test.txt');
d = d(1:frek:end,:);
%parameters = csvread('parameters.txt');
%th = parameters(:, 3)';
w=zeros(M, size(d, 2));
%w=w(:);
n = 0;
%vlezniot signal go pravime kolonski vektor (samo edna kolona)
%d=d(:);

reports=zeros(size(d));
errors=zeros(size(d));
filter_in = zeros(length(d),1);
filter_out = zeros(length(d),1);

aux2Mju = 0;

brojac = 0;
aux = 0; % momentalen pomoshen brojach, ako greshkata e pod pragot, chekaj M prakjanja
         % i posle prekini so transmisija i premini vo STAND-ALONE mode
%LMS
%MOD NA INICIJALIZACIJA (INITIALIZATION MODE)

sumaMju = zeros(1,size(d, 2));
Ex = zeros(1,size(d, 2));

for n=1:M
        w(isinf(w)) = 0;
        %uvec=d(n:1:n+M-1);
        %e(n)=d(n)-w'*uvec;
        %w=w+mu*uvec*conj(e(n));
        y(n, :)=zeros(1, size(d, 2)); 
        e(n, :)=zeros(1, size(d, 2));
        sumaMju = sumaMju + d(n, :).^2;
        % M pati prakja do sink-ot za da se inicijaliziraat pochetnite
        % vrednosti vrz koi kje mozhe da se vrshi predviduvanjeto
        brojac = brojac + 1;
end

Ex = (1/M)*sumaMju;
mu = (2./Ex)/100;

mjju = mu/M;

for n=M+1:size(d, 1)
    uvec=d(n-M:n-1, :);
    
    %uvec=uvec(:);
    %uvec = flipud(uvec);
    y(n, :) = diag(w'*uvec);
    
    e(n, :)=d(n, :)-y(n, :);
    
    errors(n,:) = 0;

%     if(n < 150) 
%         mu = 2.4985e-005;
%     else
%         mu = 1.0e-005;
%     end

    %if (e(n)>= th || e(n) <= -th)  %NORMALEN REZHIM (NORMAL MODE)
    
    
    if (sum(abs(e(n, :)) >= th) > 0)  %NORMALEN REZHIM (NORMAL MODE)
        brojac = brojac + 1;  % sekogas koga e pogolema greskata od pragot, isprati go
        %size(repmat(mu, size(uvec, 1), size(uvec, 2)))
        %size(uvec)
        %size(repmat(e(n, :), M, 1))
        w=w+repmat(mu, size(uvec, 1), 1).*uvec.*repmat(e(n, :), M, 1); % izmerenoto i azhuriraj gi tezhinite
        %mu = mu + 0.001*mu*(e(n)/100);
            aux = 0; %momentalniot brojac napravi go nula
            reports(n, :) = d(n, :);
            %errors(n, :) = e(n, :);
    else
        if(aux < M) %greskata e pod threshold ama chekame 5 posledovatelni 
            %predviduvanja pomali od pragot, pa ushte sme vo NORMAL MODE
            %ako pagja uslovot (aux < M) togash sme vo STAND-ALONE MODE
            brojac = brojac + 1;

            w=w+repmat(mu, size(uvec, 1), 1).*uvec.*repmat(e(n, :), M, 1);
            aux = aux + 1;
            reports(n, :) = d(n, :);
            %errors(n, :) = e(n, :);
            aux2Mju = 0;
        else
            d(n, :) = y(n, :); %tuka sme vo STAND-ALONE MODE
            %gi zamenuvame chitanjata so predviduvanjata
            aux2Mju = aux2Mju + 1;
            errors(n, :) = e(n, :);

        end
        %w=w+mu*uvec*conj(e(n));
    end
    if(aux2Mju > M*sqrt(M)) 
        mu = mjju;
    end
%     end
% 
end
procent = brojac/size(d, 1);
e = errors;
msqe = sum(e(:).^2)/size(d, 1);
%y=y(:);
end